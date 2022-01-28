from django.db import models, router
from django.db.models.deletion import Collector
from product.models import Shop
from user.models import User
from django.core.validators import MinValueValidator
from product.models import Product


class Order(models.Model):
    CHECKING = "CH"
    CONFIRMED = "CO"
    CANCELED = "CA"

    STATUS_CHOICES = (
        (CHECKING, "در حال بررسی"),
        (CONFIRMED, "تایید شده"),
        (CANCELED, "لغو شد"),
    )

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='orderitem')
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)], blank=True,
                                      default=0)
    total_quantity = models.IntegerField(blank=True, default=0)
    discount = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.00)], blank=True,
                                   default=0)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=CHECKING)
    is_payment = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        return f'order #{self.id} - {self.client.phone}'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)], blank=True)
    discount = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.00)], blank=True,
                                   default=0)
    quantity = models.PositiveIntegerField(default=1)
    total_item_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)],
                                           blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['product', 'order']

    def str(self):
        return self.product.name

    def save(self, *args, **kwargs):
        if self.discount < self.product.discount:
            self.discount = self.product.discount
        if not self.unit_price:
            self.unit_price = self.product.price
        self.total_item_price = self.product.price * self.quantity * (1 - self.discount)

        self.order.total_price += self.total_item_price
        self.order.total_quantity += self.quantity
        self.order.save()
        self.product.stock -= self.quantity
        self.product.save()
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.order.total_price -= self.total_item_price
        self.order.total_quantity -= self.quantity
        self.order.save()

        self.product.stock += self.quantity
        self.product.save()

        using = using or router.db_for_write(self.__class__, instance=self)
        assert self.pk is not None, (
                "%s object can't be deleted because its %s attribute is set to None." %
                (self._meta.object_name, self._meta.pk.attname)

        )
        collector = Collector(using=using)
        collector.collect([self], keep_parents=keep_parents)
        return collector.delete()
