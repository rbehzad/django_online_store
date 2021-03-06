from os import truncate
from django.contrib import admin
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils.safestring import mark_safe
from accounts.models import User
from online_store.utils import unique_slug_generator
from django.db.models.signals import pre_save


class Tag(models.Model):
    slug = models.SlugField(unique=True, max_length=120, null=True, blank=True)
    title = models.CharField(max_length=120)

    class Meta:
        unique_together = ('title', 'slug')

    def __str__(self):
        return f"Tag:{self.id}"

class ShopType(models.Model):
    slug = models.SlugField(unique=True, max_length=120, null=True, blank=True)
    title = models.CharField(max_length=120)

    class Meta:
        unique_together = ('title', 'slug')

    def __str__(self):
        return f"ShopType:{self.id}"


class Shop(models.Model):
    slug = models.SlugField(unique=True, max_length=120, null=True, blank=True)
    STATUS_CHOICES = {
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Deleted', 'Deleted'),
    }
    status = models.CharField(
        max_length= 12,
        choices=STATUS_CHOICES,
        default='Pending',
    )

    shop_type = models.ForeignKey(ShopType, on_delete=SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'slug')

    def __str__(self):
        return f"Shop:{self.id}"


class Product(models.Model):
    slug = models.SlugField(unique=True, max_length=120, null=True, blank=True)
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.IntegerField()
    tag = models.ManyToManyField(Tag)
    shop = models.ForeignKey(Shop, on_delete=CASCADE)
    amount = models.IntegerField()
    image = models.FileField()
    available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('title', 'slug')

    def admin_image(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))
    admin_image.short_description = 'Image'
    admin_image.allow_tags = True

    def __str__(self):
        return f"Product:{self.id}"

    def check_availablity(self):
        if self.amount == 0:
            self.available = False
            self.save()
        else:
            self.available = True
            self.save()


# class Image(models.Model):
#     name = models.CharField(max_length=255)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='images/')
#     default = models.BooleanField(default=False)



def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Tag)
pre_save.connect(slug_generator, sender=ShopType)
pre_save.connect(slug_generator, sender=Shop)
pre_save.connect(slug_generator, sender=Product)