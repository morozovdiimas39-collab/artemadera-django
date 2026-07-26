import json
import importlib
import re
from urllib.parse import urlsplit
from xml.etree import ElementTree

from django.contrib.staticfiles import finders
from django.db.models.signals import post_save
from django.test import Client, TestCase
from django.urls import reverse
from unittest.mock import patch

from crm.models import CrmDeal

from .direct_conversions import build_direct_conversions_csv
from .lead_notifications import signed_lead_status_token
from .models import ContactLead
from .signals import contact_lead_process


class DirectConversionsCsvTests(TestCase):
    def setUp(self):
        post_save.disconnect(
            receiver=contact_lead_process,
            sender=ContactLead,
            dispatch_uid="main_contact_lead_process",
        )

    def tearDown(self):
        post_save.connect(
            contact_lead_process,
            sender=ContactLead,
            dispatch_uid="main_contact_lead_process",
        )

    def test_unmarked_lead_is_not_exported_until_email_button_click(self):
        lead = ContactLead.objects.create(
            name="Тест",
            phone="+7 (999) 111-22-33",
            ym_client_id="123456789",
        )

        self.assertNotIn("lead_", build_direct_conversions_csv())

        token = signed_lead_status_token(lead.pk, ContactLead.DIRECT_STATUS_IN_PROGRESS)
        response = Client(HTTP_HOST="artemadera.ru").get(
            reverse("lead_direct_status", args=[token]),
            secure=True,
        )
        self.assertEqual(response.status_code, 200)

        csv_data = build_direct_conversions_csv()
        self.assertIn(f"lead_{lead.pk}", csv_data)
        self.assertIn("IN_PROGRESS", csv_data)
        self.assertIn("300.0", csv_data)

    def test_spam_lead_is_exported_as_spam_with_zero_revenue(self):
        lead = ContactLead.objects.create(
            name="Спам",
            phone="+7 (999) 222-33-44",
            direct_status=ContactLead.DIRECT_STATUS_SPAM,
        )
        self.assertIsNotNone(lead.direct_status_updated_at)

        csv_data = build_direct_conversions_csv()

        self.assertIn(f"lead_{lead.pk}", csv_data)
        self.assertIn("SPAM", csv_data)
        self.assertNotIn("300.0", csv_data)


class ContactLeadSubmitTests(TestCase):
    def test_contact_form_accepts_lead_even_when_crm_signal_fails(self):
        with patch(
            "crm.services.create_deal_from_site_lead",
            side_effect=RuntimeError("CRM unavailable"),
        ), patch("main.lead_notifications.send_lead_created_email"):
            response = Client(HTTP_HOST="artemadera.ru").post(
                "/",
                {
                    "form_type": "contact",
                    "name": "Тест",
                    "phone": "+7 (999) 333-44-55",
                    "message": "Проверка заявки",
                    "from_block": "contact",
                },
                HTTP_X_REQUESTED_WITH="XMLHttpRequest",
                secure=True,
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["ok"], True)
        self.assertTrue(
            ContactLead.objects.filter(phone="+7 (999) 333-44-55").exists()
        )

    def test_contact_form_persists_attribution_creates_crm_deal_and_calls_email(self):
        with patch("main.lead_notifications.send_lead_created_email") as send_email:
            response = Client(HTTP_HOST="artemadera.ru").post(
                "/pokraska",
                {
                    "form_type": "contact",
                    "name": "QA ArteMadera",
                    "phone": "+7 (999) 444-55-66",
                    "message": "Проверка CRM",
                    "from_block": "contact",
                    "utm_source": "qa",
                    "utm_campaign": "seo-release",
                    "yclid": "test-click-id",
                    "landing_page": "https://artemadera.ru/pokraska?utm_source=qa",
                    "page_url": "https://artemadera.ru/pokraska",
                },
                HTTP_X_REQUESTED_WITH="XMLHttpRequest",
                secure=True,
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        lead = ContactLead.objects.get(phone="+7 (999) 444-55-66")
        self.assertEqual(lead.utm_source, "qa")
        self.assertEqual(lead.utm_campaign, "seo-release")
        self.assertEqual(lead.yclid, "test-click-id")
        deal = CrmDeal.objects.get(site_lead=lead)
        self.assertEqual(response.json()["crm_deal_id"], deal.pk)
        self.assertIn("utm_source: qa", deal.description)
        self.assertIn("yclid: test-click-id", deal.description)
        send_email.assert_called_once_with(lead)

    def test_ajax_contact_form_rejects_missing_phone_without_creating_lead(self):
        response = Client(HTTP_HOST="artemadera.ru").post(
            "/",
            {"form_type": "contact", "name": "Без телефона"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            secure=True,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"ok": False, "error": "phone_required"})
        self.assertFalse(ContactLead.objects.filter(name="Без телефона").exists())


class CanonicalHostMiddlewareTests(TestCase):
    def test_http_apex_redirects_to_https(self):
        response = Client(HTTP_HOST="artemadera.ru").get("/shlifovka?utm_source=test")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response["Location"],
            "https://artemadera.ru/shlifovka?utm_source=test",
        )

    def test_https_apex_is_not_redirected(self):
        response = Client(HTTP_HOST="artemadera.ru").get("/robots.txt", secure=True)

        self.assertEqual(response.status_code, 200)

    def test_forwarded_https_is_not_redirected(self):
        response = Client(HTTP_HOST="artemadera.ru").get(
            "/robots.txt",
            HTTP_X_FORWARDED_PROTO="https",
        )

        self.assertEqual(response.status_code, 200)

    def test_www_and_legacy_domain_redirect_to_ru_https(self):
        hosts = (
            "www.artemadera.ru",
            "artemadera.su",
            "www.artemadera.su",
        )
        for host in hosts:
            with self.subTest(host=host):
                response = Client(HTTP_HOST=host).get(
                    "/pokraska?yclid=123",
                    secure=True,
                )
                self.assertEqual(response.status_code, 301)
                self.assertEqual(
                    response["Location"],
                    "https://artemadera.ru/pokraska?yclid=123",
                )

    def test_legacy_path_redirect_is_single_hop_and_preserves_query(self):
        response = Client(HTTP_HOST="artemadera.su").get(
            "/otdelka/?gclid=abc",
            secure=True,
        )

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response["Location"],
            "https://artemadera.ru/otdelochnye-raboty?gclid=abc",
        )

    def test_public_service_trailing_slash_redirects_to_canonical_path(self):
        response = Client(HTTP_HOST="artemadera.ru").get(
            "/pokraska/",
            secure=True,
        )

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "https://artemadera.ru/pokraska")


class SeoEndpointTests(TestCase):
    def test_robots_declares_canonical_sitemap_and_tracking_clean_params(self):
        response = Client(HTTP_HOST="artemadera.ru").get("/robots.txt", secure=True)

        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn("Sitemap: https://artemadera.ru/sitemap.xml", body)
        self.assertIn("Disallow: /admin/", body)
        self.assertIn("Clean-param: utm_source", body)
        self.assertIn("yclid", body)
        self.assertIn("gclid", body)

    def test_sitemap_is_valid_and_contains_only_canonical_replacement_paths(self):
        response = Client(HTTP_HOST="artemadera.ru").get("/sitemap.xml", secure=True)

        self.assertEqual(response.status_code, 200)
        root = ElementTree.fromstring(response.content)
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = {node.text for node in root.findall("sm:url/sm:loc", namespace)}
        self.assertIn("https://artemadera.ru/", locations)
        self.assertIn("https://artemadera.ru/shlifovka", locations)
        self.assertNotIn(
            "https://artemadera.ru/otdelka/shlifovka/bani-i-sauny",
            locations,
        )
        self.assertNotIn(
            "https://artemadera.ru/otdelka/shlifovka/konsyerzhnaya",
            locations,
        )
        self.assertTrue(all(url.startswith("https://artemadera.ru/") for url in locations))

    def test_page_has_https_canonical_and_valid_nonduplicated_schema(self):
        response = Client(HTTP_HOST="artemadera.ru").get("/pokraska", secure=True)

        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn(
            '<link rel="canonical" href="https://artemadera.ru/pokraska"',
            body,
        )
        scripts = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>',
            body,
            flags=re.DOTALL,
        )
        schemas = [json.loads(script) for script in scripts]
        flattened = []
        for schema in schemas:
            flattened.extend(schema if isinstance(schema, list) else [schema])
        schema_types = [schema.get("@type") for schema in flattened]
        self.assertIn("LocalBusiness", schema_types)
        self.assertIn("WebSite", schema_types)
        self.assertIn("Service", schema_types)
        self.assertLessEqual(schema_types.count("FAQPage"), 1)

    def test_every_sitemap_url_renders_with_one_self_referential_canonical(self):
        client = Client(HTTP_HOST="artemadera.ru")
        sitemap = client.get("/sitemap.xml", secure=True)
        root = ElementTree.fromstring(sitemap.content)
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        for location_node in root.findall("sm:url/sm:loc", namespace):
            location = location_node.text
            path = urlsplit(location).path
            with self.subTest(path=path):
                response = client.get(path, secure=True)
                self.assertEqual(response.status_code, 200)
                body = response.content.decode()
                canonical_hrefs = re.findall(
                    r'<link rel="canonical" href="([^"]+)"',
                    body,
                )
                self.assertEqual(canonical_hrefs, [location])


class StaticFallbackTests(TestCase):
    def test_webp_migration_targets_exist_and_decode(self):
        migration = importlib.import_module(
            "main.migrations.0089_switch_static_png_fallbacks_to_webp"
        )
        from PIL import Image

        for static_path in migration.REPLACEMENTS.values():
            with self.subTest(static_path=static_path):
                resolved = finders.find(static_path)
                self.assertIsNotNone(resolved)
                with Image.open(resolved) as image:
                    image.verify()
