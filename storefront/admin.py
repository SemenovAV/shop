from django.contrib import admin

from storefront.models import Product, Article, Category, Section


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'category', 'admin_img']
    list_filter = ['available', 'category', 'created', 'updated', ]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['title', 'section']
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    filter_horizontal = ['products']
    list_display = ['title', 'created']
    list_filter = ['created']


@admin.register(Section)
class AdminSection(admin.ModelAdmin):
    list_display = ['title', 'parent_section']
    list_editable = ['parent_section']
    prepopulated_fields = {"slug": ("title",)}
