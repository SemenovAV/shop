from django.db import models
from django.utils.translation import gettext_lazy as _

from storefront.models import Product
from users.models import CustomUser


class Order(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created')

    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated')
    )
    paid = models.BooleanField(
        default=False,
        verbose_name=_('paid')

    )

    class Meta:
        ordering = ('-created',)
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return f'{_("Order")} {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name=_('order')
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name=_('product')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('price')
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('quantity')
    )

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity
