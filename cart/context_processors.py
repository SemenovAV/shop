from .cart import Cart
from .forms import CartAddProductForm, CartAddUnitForm


def cart(request):
    return {
        'cart': Cart(request),
        'form': CartAddProductForm,
        'unit_form': CartAddUnitForm,
        'url': request.path,
    }
