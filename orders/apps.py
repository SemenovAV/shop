from django.apps import AppConfig
from django.utils.translation import gettext as _


class OrdersConfig(AppConfig):
    name = 'orders'
    verbose_name = _('orders')
