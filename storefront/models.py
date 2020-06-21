from django.db import models
from django.utils.translation import gettext_lazy as _


def get_all_ancestors(parent, url=''):
    url = f'{parent.slug}/{url}'
    if parent.parent_category:
        return get_all_ancestors(parent.parent_category, url)
    else:
        return f'{url}'


class Product(models.Model):
    title = models.CharField(
        max_length=255,
        db_index=True,
        unique=True,
        verbose_name=_('title')
    )
    img = models.ImageField(
        upload_to='img',
        verbose_name=_('image')
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('price')
    )
    stock = models.PositiveIntegerField(
        verbose_name=_('stock')
    )
    available = models.BooleanField(
        default=True
    )
    category = models.ForeignKey(
        'SubCategory',
        on_delete=models.PROTECT,
        related_name='products',
        null=True,
        blank=True,
        verbose_name=_('category')

    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created')
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated')
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name=_('slug')
    )

    def thumbnail(self):
        if self.img:
            from django.utils.safestring import mark_safe
            return mark_safe(f'<a href="{self.img.url}" target="_blank"><img src="{self.img.url}" width="50"/></a>')

    def get_absolute_url(self):
        url = f'{self.slug}'
        if self.category:
            return get_all_ancestors(self.category, url)
        else:
            return f'{url}'

    class Meta:
        ordering = ('price',)
        index_together = (('id', 'slug'),)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(
        max_length=100,
        db_index=True,
        unique=True,
        verbose_name=_('title')
    )
    parent_category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='categories',
        verbose_name=_('parent category')
    )
    order = models.IntegerField(
        default=0,
        db_index=True,
        verbose_name=_('order')
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name=_('slug')
    )

    class Meta:
        unique_together = ('parent_category', 'slug')

    def get_subcategory(self):
        return Category.objects.all().prefetch_related().filter(parent_category_id=self.id)

    def get_absolute_url(self):
        url = f'{self.slug}'
        if self.parent_category:
            return get_all_ancestors(self.parent_category, url)
        else:
            return f'{url}'


class ParentCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent_category__isnull=True)


class ParentCategory(Category):
    objects = ParentCategoryManager()

    def __str__(self):
        if self.parent_category:
            return f'{self.parent_category.title} - {self.title}'
        else:
            return self.title

    class Meta:
        proxy = True
        ordering = ('order', 'title')
        verbose_name = _('parent category')
        verbose_name_plural = _('parent categories')


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent_category__isnull=False)


class SubCategory(Category):
    objects = SubCategoryManager()

    def __str__(self):
        return f'{self.parent_category.title} - {self.title}'

    class Meta:
        proxy = True
        ordering = ('order', 'title')
        verbose_name = _('subcategory')
        verbose_name_plural = _('subcategories')


class Article(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name=_('title')
    )
    text = models.TextField(
        verbose_name=_('text')
    )
    products = models.ManyToManyField(
        'Product',
        related_name='articles',
        verbose_name=_('products')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created')
    )

    class Meta:
        ordering = ('created',)
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def __str__(self):
        return self.title
