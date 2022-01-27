# Generated by Django 3.2.11 on 2022-01-25 08:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_alter_shop_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('total_quantity', models.IntegerField(blank=True, default=0)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('status', models.CharField(choices=[('py', 'در حال بررسی'), ('CO', 'تایید شده'), ('CA', 'لغو شد')], default='py', max_length=9)),
                ('is_payment', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total_item_price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'unique_together': {('product', 'order')},
            },
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='order.OrderItem', to='product.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.shop'),
        ),
    ]