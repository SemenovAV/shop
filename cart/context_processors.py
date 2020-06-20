from .cart import Cart
from .forms import CartAddProductForm


def cart(request):
    return {
        'cart': Cart(request),
        'form': CartAddProductForm,
        'url': request.path,
    }
