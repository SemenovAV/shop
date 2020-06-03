from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField(upload_to='img')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200)

    def admin_img(self):
        if self.img:
            from django.utils.safestring import mark_safe
            return mark_safe(f'<a href="{self.img.url}" target="_blank"><img src="{self.img.url}" width="50"/></a>')

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title


class Section(models.Model):
    title = models.CharField(max_length=100)
    parent_section = models.ForeignKey(
        'Section',
        on_delete=models.PROTECT,
        related_name='subsections',
        blank=True,
        null=True
    )
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    products = models.ManyToManyField('Product', related_name='articles')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title
