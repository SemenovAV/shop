from .cart import Cart
from .forms import CartAddProductForm, CartAddUnitSet


def cart(request):
    return {
        'cart': Cart(request),
        'form': CartAddProductForm,
        'unit_form': CartAddUnitSet,
        'url': request.path,
    }
