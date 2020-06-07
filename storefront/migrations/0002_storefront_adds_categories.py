# Generated by Django 2.2.12 on 2020-06-07 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0001_storefront_create_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, unique=True)),
                ('order', models.IntegerField(db_index=True, default=0)),
                ('slug', models.SlugField(max_length=200)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='storefront.Category')),
            ],
            options={
                'unique_together': {('parent_category', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='ParentCategory',
            fields=[
            ],
            options={
                'verbose_name': 'parent category',
                'verbose_name_plural': 'parent categories',
                'ordering': ('order', 'title'),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('storefront.category',),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
            ],
            options={
                'verbose_name': 'subcategory',
                'verbose_name_plural': 'subcategories',
                'ordering': ('order', 'title'),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('storefront.category',),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='storefront.SubCategory'),
        ),
    ]