from django.db import models
from django.db.models.deletion import CASCADE
from accounts.models import User
from shop_managing.models import *
from online_store.utils import unique_slug_generator
from django.db.models.signals import pre_save


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='carts')
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=120, null=True, blank=True)
    STATUS_CHOICES = {
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Canceled', 'Canceled'),
        ('Paid', 'Paid'),
    }
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='Pending',
    )
    
    total_cost = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop, on_delete=SET_NULL, null=True, related_name='carts')
    

    class Meta:
        unique_together = ('title', 'slug')

    def __str__(self):
        return f"Cart:id:{self.id}"

    def get_total_price(self):
        return sum(item.get_cost() for item in self.cart_item.all())

    def get_products_number(self):
        return sum(item.amount for item in self.cart_item.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=CASCADE)
    amount = models.IntegerField(default=1)
    total_cost = models.IntegerField(default=0)

    def __str__(self):
        return f"cartitem:{self.id}"

    def get_cost(self):
        return self.amount * self.product.price


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Cart)
