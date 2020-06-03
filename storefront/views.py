from django.shortcuts import render
from django.views.generic import ListView
from storefront.models import Article


class StoreFrontView(ListView):
    template_name = 'index.html'
    model = Article
    queryset = Article.objects.all().prefetch_related()
    context_object_name = 'articles'
    paginate_by = 10

