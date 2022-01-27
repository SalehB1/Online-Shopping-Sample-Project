import random

from django.core.validators import MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.html import format_html
from .Managers import UnDeletedShop, DeletedShop

from user.models import User


# Create your models here.
class Shop(models.Model):
    SUPERMARKET = "SU"
    HYPERMARKET = "HY"
    VEGETABLESSTORE = "VS"
    FRUITSTORE = "FS"
    ORGANICSTORE = "OS"
    CONVENIENCESTORE = "CS"

    TYPE_CHOICES = (
        (SUPERMARKET, "سوپر مارکت"),
        (HYPERMARKET, "هایپر مارکت"),
        (VEGETABLESSTORE, "فروشگاه سبزیجات"),
        (FRUITSTORE, "میوه فروشی"),
        (ORGANICSTORE, "فروشگاه ارگانیک"),
        (CONVENIENCESTORE, "خواربارفروشی"),
    )
    slug = models.SlugField(max_length=60, blank=True, unique=True, verbose_name='اسلاگ')
    name = models.CharField(max_length=50, verbose_name='نام فروشگاه')
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=SUPERMARKET, verbose_name='نوع فروشگاه')
    address = models.TextField(verbose_name='آدرس')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='فروشنده')
    is_confirmed = models.BooleanField(default=False, verbose_name='تایید شده است')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده')

    objects = models.Manager()
    Deleted = DeletedShop()
    UnDeleted = UnDeletedShop()

    def str(self):
        return f'{self.seller.username} فروشگاه {self.id} با نام {self.name} برای یوزر '

    def random_number_generator(self):
        return '_' + str(random.randint(1000, 9999))

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name) + '_' + str.lower(self.type).replace(" ", "_")
            while Shop.objects.filter(slug=self.slug):
                self.slug = slugify(self.name)
                self.slug += self.random_number_generator()
        return super().save(*args, **kwargs)


class Product(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='productImage/')
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    discount = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0.00)], blank=True,
                                   default=0)
    sales = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    stock = models.PositiveIntegerField(default=0, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)], blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag', blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_products')
    is_active = models.BooleanField(default=False, verbose_name='shop active')
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def random_number_generator(self):
        return '-' + str(random.randint(1000, 9999))

    def image_tag(self):
        return format_html('<img src="{}"  width="50" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.image)
            while Product.objects.filter(slug=self.slug):
                self.slug = slugify(self.image)
                self.slug += self.random_number_generator()

        if self.stock == 0:
            self.is_active = False
        if not self.sales:
            price = self.price
            self.sales = price - ((price * self.discount) / 100)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50, verbose_name='title category')

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='title tag')

    class Meta:
        ordering = ['title', ]

    def __str__(self):
        return self.title
