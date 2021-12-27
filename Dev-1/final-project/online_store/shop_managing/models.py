from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from accounts.models import User

class ShopType(models.Model):
    STATUS_CHOICES = {
        ('dai', 'dairy'),
        ('dru', 'drugstore'),
        ('swe', 'sweetshop'),
        ('boo', 'bookshop'),
    }
    title = models.CharField(max_length=120)
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
    )
    def __str__(self) -> str:
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.title


class Shop(models.Model):
    STATUS_CHOICES = {
        ('pen', 'Pending'),
        ('con', 'Confirmed'),
        ('del', 'Deleted'),
    }
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='pen',
    )
    title = models.CharField(max_length=120)
    shop_type = models.ForeignKey(ShopType, on_delete=SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=120)
    price = models.IntegerField()
    tag = models.ManyToManyField(Tag)
    shop = models.ForeignKey(Shop, on_delete=CASCADE)
    amount = models.IntegerField()
    image = models.ImageField(upload_to="")

    def __str__(self) -> str:
        return self.title

