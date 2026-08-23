import os

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def ensure_default_site(sender, **kwargs):
    from django.contrib.sites.models import Site

    domain = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '127.0.0.1:8000')
    Site.objects.update_or_create(
        pk=1,
        defaults={
            'domain': domain,
            'name': 'Digital Library',
        },
    )


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        post_migrate.connect(ensure_default_site, sender=self)