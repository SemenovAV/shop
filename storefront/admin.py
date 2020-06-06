from django.contrib import admin

from storefront.models import Product, Article, SubCategory, ParentCategory
from .forms import SubCategoryForm


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'thumbnail']
    list_filter = ['available', 'created', 'updated', ]
    prepopulated_fields = {"slug": ("title",)}


class ParentCategoryInline(admin.TabularInline):
    model = ParentCategory
    extra = 1


@admin.register(ParentCategory)
class ParentCategoryAdmin(admin.ModelAdmin):
    exclude = ('parent_category', )
    inlines = (ParentCategoryInline,)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    filter_horizontal = ['products']
    list_display = ['title', 'created']
    list_filter = ['created']
