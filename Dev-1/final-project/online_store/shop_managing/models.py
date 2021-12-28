from os import truncate
from django.contrib import admin
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils.safestring import mark_safe
from accounts.models import User

class Tag(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return f"tag: {self.title}"

class ShopType(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return f"shop type: {self.title}"


class Shop(models.Model):
    STATUS_CHOICES = {
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Deleted', 'Deleted'),
    }
    status = models.CharField(
        max_length= 10,
        choices=STATUS_CHOICES,
        default='Pending',
    )

    shop_type = models.OneToOneField(ShopType, on_delete=SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"shop:{self.shop_type}:{self.title}"


class Product(models.Model):
    title = models.CharField(max_length=120)
    price = models.IntegerField()
    tag = models.ManyToManyField(Tag, null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=CASCADE)
    amount = models.IntegerField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def admin_image(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))
    admin_image.short_description = 'Image'
    admin_image.allow_tags = True


    def __str__(self):
        return f"product: {self.title}"

