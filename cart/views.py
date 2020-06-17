from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import FormView, RedirectView, TemplateView

from storefront.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartAddUnitForm


class CartAdd(FormView):
    template_name = 'cart/detail.html'
    form_class = CartAddProductForm
    cart = None
    product = None

    def post(self, request, *args, **kwargs):
        self.success_url = kwargs.get('url')
        print(self.success_url)
        self.cart = Cart(request)
        self.product = get_object_or_404(Product, id=kwargs.get('product_id'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.cart.add(product=self.product)
        self.cart.save()
        return super().form_valid(form)


class CartAddUnit(FormView):
    template_name = 'cart/detail.html'
    form_class = CartAddUnitForm
    cart = None
    product = None

    def get(self, request, *args, **kwargs):
        print("!!!!!!!!")
        print(get_object_or_404(Product, id=kwargs.get('product_id')))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.success_url = kwargs.get('url')
        self.cart = Cart(request)
        self.product = get_object_or_404(Product, id=kwargs.get('product_id'))
        context = self.get_context_data()
        context['stock'] = range(self.product.stock)
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


# def cart_remove(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect('cart:cart_detail')

class CartDetail(TemplateView):
    template_name = 'cart/detail.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return super().get(request, cart=cart, *args, **kwargs)

# def cart_detail(request):
#     cart = Cart(request)
#     return render(request, 'cart/detail.html', {'cart': cart})