from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import FormView, RedirectView

from storefront.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartAddUnitFormSet


class CartAdd(FormView):
    template_name = 'cart/detail.html'
    form_class = CartAddProductForm
    cart = None
    product = None

    def post(self, request, *args, **kwargs):
        self.success_url = kwargs.get('url')

        self.cart = Cart(request)
        self.product = get_object_or_404(Product, id=kwargs.get('product_id'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.cart.add(product=self.product)
        self.cart.save()
        return super().form_valid(form)


class CartRemove(RedirectView):
    template_name = 'cart/detail.html'
    cart = None
    pattern_name = 'cart:cart_detail'

    def get_redirect_url(self, *args, **kwargs):
        return reverse(self.pattern_name)

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id', 0)
        self.cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        self.cart.remove(product)
        return super().get(request, *args, **kwargs)


class CartDetail(FormView):
    template_name = 'cart/detail.html'
    form_class = CartAddUnitFormSet

    def get(self, request, *args, **kwargs):

        referer = request.META.get('HTTP_REFERER')
        if referer:
            referer = referer.split('/')
            referer_host = referer[2]
            referer_path = '/'.join(referer[3:])
            host = request.get_host()
            print(referer_path, referer_host)
            self.extra_context = {
                'referer': referer_path if referer and referer[2] == host else '/'

            }
        else:
            self.extra_context = {
                'referer':  '/'

            }


        self.cart = Cart(request)
        self.initial = []
        for item in self.cart:
            self.initial.append({
                'id': item['product'].id,
                'price': item['price'],
                'quantity': item['quantity'],
                'title': item['product'].title,
                'total_price': item['total_price'],
                'img': item['product'].img.url
            })
        return super().get(request, cart=self.cart, *args, **kwargs)

    def get_success_url(self):
        return reverse('cart:cart_detail')

    def form_valid(self, form):
        cart = Cart(self.request)
        data = form.cleaned_data
        for item in data:
            cart.add_unit(str(item.get('id')), item.get('quantity'))

        return super(CartDetail, self).form_valid(form)
