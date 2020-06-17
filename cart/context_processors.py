from .cart import Cart
from .forms import CartAddProductForm,CartAddUnitFormSet


def cart(request):
    return {
        'cart': Cart(request),
        'form': CartAddProductForm,
        'unit_form': CartAddUnitFormSet,
        'url': request.path,
    }
