from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from accounts.models import User
from shop_managing.models import *
from online_store.utils import unique_slug_generator
from django.db.models.signals import pre_save


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=120, null=True, blank=True)
    STATUS_CHOICES = {
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Deleted', 'Deleted'),
        ('Paid', 'Paid'),
    }
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='pending',
    )
    
    total_cost = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop, on_delete=SET_NULL, null=True)

    class Meta:
        unique_together = ('title', 'slug')

    def __str__(self):
        return f"Cart:{self.title}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    amount = models.IntegerField(default=1)
    total_cost = models.IntegerField(default=0)

    def __str__(self):
        return self.product.title


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Cart)
