from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.deletion import CASCADE
from .managers import MyUserManager


class User(AbstractBaseUser):
	username = models.CharField(max_length=100, unique=True, blank=True, null=True)
	email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
	fullname = models.CharField(max_length=100, blank=True, null=True)
	phone_number = models.CharField(max_length=9, unique=True, blank=True, null=True)
	is_admin = models.BooleanField(default=False)
	is_seller = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	objects = MyUserManager()
	USERNAME_FIELD = 'email'

	REQUIRED_FIELDS = ['fullname']

	def __str__(self):
		return self.fullname

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin