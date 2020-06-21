from django.apps import AppConfig
from django.utils.translation import gettext as _


class StorefrontConfig(AppConfig):
    name = 'storefront'
    verbose_name = _('storefront')
