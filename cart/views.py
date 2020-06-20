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


class CartAddUnit(FormView):
    template_name = 'cart/detail.html'
    form_class = CartAddUnitFormSet

    def post(self, request, *args, **kwargs):
        print(request, args, kwargs)
        return super().post(request, *args, **kwargs)






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


# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect('cart:cart_detail')

class CartDetail(FormView):
    template_name = 'cart/detail.html'
    form_class = CartAddUnitFormSet

    def get(self, request, *args, **kwargs):
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
            cart.add_unit(str(item.get('id')),item.get('quantity'))

        return super(CartDetail,self).form_valid(form)
    # def get_form(self, form_class=None):
    #     """Return an instance of the form to be used in this view."""
    #     if form_class is None:
    #         form_class = self.get_form_class()
    #     print(form_class(**self.get_form_kwargs()))
    #     return form_class(**self.get_form_kwargs())
    #
    # def get_form_kwargs(self):
    #     """Return the keyword arguments for instantiating the form."""
    #     kwargs = {
    #         'initial': self.get_initial(),
    #         'prefix': self.get_prefix(),
    #     }
    #
    #     if self.request.method in ('POST', 'PUT'):
    #         kwargs.update({
    #             'initial': self.get_initial(),
    #             'data': self.request.POST,
    #             })
    #     return kwargs
