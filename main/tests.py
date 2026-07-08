from django.db.models.signals import post_save
from django.test import Client, TestCase
from django.urls import reverse
from unittest.mock import patch

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
            reverse("lead_direct_status", args=[token])
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
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["ok"], True)
        self.assertTrue(
            ContactLead.objects.filter(phone="+7 (999) 333-44-55").exists()
        )
