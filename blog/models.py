# from django.contrib.auth.models import User
# from django.conf.settings import AUTH_USER_MODEL as User
from accounts.models import User

from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.signals import pre_save
from django.utils import tree
from online_store.utils import unique_slug_generator


class Tag(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=120, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'slug')

    def __str__(self) -> str:
        return f"tag: {self.title}"


class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=120, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'slug')

    def __str__(self):
        return f"category: {self.title}"


class Post(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="images/")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=120, null=True, blank=True)

    author = models.ForeignKey(User, on_delete=CASCADE)
    category = models.ManyToManyField(Category)
    tag = models.ManyToManyField(Tag, blank=True, null=True)

    class Meta:
        unique_together = ('title', 'slug')

    def __str__(self):
        return f"post: {self.title}"


class Comment(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"comment: {self.title}"


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)
pre_save.connect(slug_generator, sender=Category)
pre_save.connect(slug_generator, sender=Tag)