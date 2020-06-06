from django.db import models


class Product(models.Model):
    title = models.CharField(
        max_length=255,
        db_index=True,
        unique=True
    )
    img = models.ImageField(
        upload_to='img'
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    stock = models.PositiveIntegerField()
    available = models.BooleanField(
        default=True
    )
    category = models.ForeignKey(
        'SubCategory',
        on_delete=models.PROTECT,
        related_name='products',
        null=True,
        blank=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    slug = models.SlugField(
        max_length=200
    )

    def thumbnail(self):
        if self.img:
            from django.utils.safestring import mark_safe
            return mark_safe(f'<a href="{self.img.url}" target="_blank"><img src="{self.img.url}" width="50"/></a>')

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}'

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(
        max_length=100,
        db_index=True,
        unique=True
    )
    parent_category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    order = models.IntegerField(
        default=0,
        db_index=True
    )
    slug = models.SlugField(
        max_length=200
    )

    def get_subcategory(self):
        return Category.objects.all().prefetch_related().filter(parent_category_id=self.id)

    def get_absolute_url(self):
        if self.parent_category:
            return f'/{self.parent_category.slug}/{self.slug}/'
        else:
            return f'/{self.slug}/'




class ParentCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent_category__isnull=True)


class ParentCategory(Category):
    objects = ParentCategoryManager()

    def __str__(self):
        return self.title


    class Meta:
        proxy = True
        ordering = ('order', 'title')
        verbose_name = 'parent category'
        verbose_name_plural = 'parent categories'


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
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'


class Article(models.Model):
    title = models.CharField(
        max_length=100
    )
    text = models.TextField()
    products = models.ManyToManyField(
        'Product',
        related_name='articles'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ('created',)
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title
