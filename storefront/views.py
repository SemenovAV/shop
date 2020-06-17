from django.views.generic import ListView
from django.utils.html import escape
from cart.forms import CartAddProductForm

from storefront.models import Article, Product


class MainView(ListView):
    template_name = 'index.html'
    model = Article
    queryset = Article.objects.all()
    context_object_name = 'articles'
    paginate_by = 10


class StoreFrontView(ListView):
    model = Product

    def get(self, request, *args, **kwargs):
        data = [escape(elem) for elem in request.path.split('/')]
        url = data[-2]
        self.extra_context = {
            'active': data,
            }
        if self.model.objects.filter(slug=url).exists():
            self.template_name = 'product.html'
            self.queryset = self.model.objects.filter(slug=url).first()
            self.context_object_name = 'product'
        elif self.model.objects.filter(category__slug=url).exists():
            self.paginate_by = 12
            self.template_name = 'products.html'
            self.queryset = self.model.objects.filter(category__slug=url)
            self.context_object_name = 'products'
        else:
            self.template_name = 'products.html'
            self.queryset = self.model.objects.filter(category__slug=url)
            self.context_object_name = 'products'
        return super(StoreFrontView, self).get(request, *args, **kwargs)



