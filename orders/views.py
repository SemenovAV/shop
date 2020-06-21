from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem
from users.models import CustomUser


class OrderCreate(CreateView):
    template_name = 'orders/order/create.html'
    form_class = OrderCreateForm
    request = None
    args = None
    kwargs = None
    user = None
    cart = None

    def setup(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = request.user
        self.cart = Cart(request)
        self.extra_context = {
            'cart': self.cart
        }

    def get_success_url(self):
        return reverse('orders:order_ok')

    @login_required()
    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = CustomUser.objects.get(pk=self.request.user.pk)
        order.save()
        order = form.save()
        for item in self.cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
        self.cart.clear()
        return HttpResponseRedirect(self.get_success_url())


class OrderOk(TemplateView):
    template_name = 'orders/order/created.html'
