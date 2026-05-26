import sys

from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from . import signals  # noqa: F401 — уведомления о ContactLead

        # Only auto-migrate on runserver — avoids SQLite locks during makemigrations/migrate
        if 'runserver' not in sys.argv:
            return

        from django.db import connection
        from django.core.management import call_command

        try:
            tables = connection.introspection.table_names()
        except Exception:
            return

        pending = []
        if 'main_calculatorconfig' not in tables:
            pending.append('0002_calculator')
        if 'main_portfoliosection' not in tables:
            pending.append('0003_portfolio')
        if 'main_experiencesection' not in tables:
            pending.append('0004_experience')
        if 'main_reviewssection' not in tables:
            pending.append('0005_reviews')
        if 'main_workprocesssection' not in tables:
            pending.append('0006_process_contact')
        if 'main_faqsection' not in tables:
            pending.append('0007_faq_beforeafter')
        if 'main_portfolioprojectimage' not in tables:
            pending.append('0008_portfolio_cases')
        if 'main_blogsection' not in tables:
            pending.append('0009_blog')

        for migration in pending:
            try:
                call_command(
                    'migrate', 'main', migration, verbosity=0, interactive=False
                )
            except Exception:
                pass
