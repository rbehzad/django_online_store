from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from accounts.models import User
from shop_managing.models import *


class Cart(models.Model):
    STATUS_CHOICES = {
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('deleted', 'Deleted'),
        ('paid', 'Paid'),
    }
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='pending',
    )
    user = models.ForeignKey(User, on_delete=CASCADE)
    total_cost = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart:{self.user.fullname}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=CASCADE)
    product = models.OneToOneField(Product, on_delete=CASCADE)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return f"CartItem:{self.product.title}"
