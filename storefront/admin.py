from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from storefront.models import Product, Article, SubCategory, ParentCategory
from .forms import SubCategoryForm


class InlineChangeList(object):
    can_show_all = True
    multi_page = True
    get_query_string = ChangeList.__dict__['get_query_string']

    def __init__(self, request, page_num, paginator):
        self.show_all = 'all' in request.GET
        self.page_num = page_num
        self.paginator = paginator
        self.result_count = paginator.count
        self.params = dict(request.GET.items())


class MyInline(admin.TabularInline):
    per_page = 10
    template = 'admin/my_tabular.html'
    model = Product
    fields = ['title', 'description', 'price']

    list_filter = ['available', 'created', 'updated' ]
    extra = 0
    can_delete = False

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(MyInline, self).get_formset(
            request, obj, **kwargs)

        class PaginationFormSet(formset_class):
            def __init__(self, *args, **kwargs):
                super(PaginationFormSet, self).__init__(*args, **kwargs)

                qs = self.queryset
                paginator = Paginator(qs, self.per_page)
                try:
                    page_num = int(request.GET.get('page', ['0'])[0])
                except ValueError:
                    page_num = 0

                try:
                    page = paginator.page(page_num + 1)
                except (EmptyPage, InvalidPage):
                    page = paginator.page(paginator.num_pages)

                self.page = page
                self.cl = InlineChangeList(request, page_num, paginator)
                self.paginator = paginator

                if self.cl.show_all:
                    self._queryset = qs
                else:
                    self._queryset = page.object_list

        PaginationFormSet.per_page = self.per_page
        return PaginationFormSet


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'category', 'thumbnail']
    search_fields = ['title']
    list_per_page = 30
    list_filter = ['available', 'created', 'updated', 'category']
    prepopulated_fields = {"slug": ("title",)}


class ParentCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


class SubCategoryInline(admin.TabularInline):
    model = Product

    fields = ['title', ]

    list_filter = ['available', 'created', 'updated', ]
    extra = 0


@admin.register(ParentCategory)
class ParentCategoryAdmin(admin.ModelAdmin):
    exclude = ('parent_category',)
    inlines = (ParentCategoryInline,)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm
    inlines = (ParentCategoryInline, MyInline)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    filter_horizontal = ['products']
    list_display = ['title', 'created']
    list_filter = ['created']
