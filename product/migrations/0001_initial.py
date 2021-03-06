# Generated by Django 3.2.11 on 2022-01-27 08:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title category')),
                ('sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title tag')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=60, unique=True, verbose_name='اسلاگ')),
                ('name', models.CharField(max_length=50, verbose_name='نام فروشگاه')),
                ('type', models.CharField(choices=[('SU', 'سوپر مارکت'), ('HY', 'هایپر مارکت'), ('VS', 'فروشگاه سبزیجات'), ('FS', 'میوه فروشی'), ('OS', 'فروشگاه ارگانیک'), ('CS', 'خواربارفروشی')], default='SU', max_length=2, verbose_name='نوع فروشگاه')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='تایید شده است')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='حذف شده')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='فروشنده')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='productImage/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('sales', models.DecimalField(blank=True, decimal_places=2, max_digits=12)),
                ('stock', models.PositiveIntegerField(blank=True, default=0)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='shop active')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_products', to='product.shop')),
                ('tag', models.ManyToManyField(blank=True, to='product.Tag')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
