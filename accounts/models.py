import random, string, uuid
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from accounts.api.sender import send_otp


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None, phone_number=None, is_active=True, is_staff=False, is_superuser=False, is_seller=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            seller=is_seller,
        )
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.superuser = is_superuser
        # user_obj.seller = is_seller
        user_obj.set_password(password)    # change user password
        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, email, password=None):
        user_obj = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user_obj

    def create_superuser(self, email, password=None):
        user_obj = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        return user_obj


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=False, blank=False, unique=True, max_length=80, verbose_name='Email')
    first_name = models.CharField(null=True, blank=True, max_length=80, verbose_name='First Name')
    last_name = models.CharField(null=True, blank=True, max_length=80, verbose_name='Last Name')
    phone_number = models.CharField(max_length=13, verbose_name='Phone Number', unique=True)
    active = models.BooleanField(default=True, verbose_name='Is Active')
    staff = models.BooleanField(default=False, verbose_name='Is Staff')
    superuser = models.BooleanField(default=False, verbose_name='Is Super User')
    seller = models.BooleanField(default=False, verbose_name='Is Seller')
    phone_number_confirmation = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    USERNAME_FIELD = 'email'    # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []    # python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_seller(self):
        return self.seller


class OtpRequestQuerySet(models.QuerySet):
    def is_valid(self, receiver, request, password):
        current_time = timezone.now()
        result =  self.filter(
            receiver=receiver,
            request_id=request,
            password=password,
            created__lt=current_time,
            created__gt=current_time-timedelta(seconds=120),

        ).exists()
        
        print(result)
        return result


class OTPManager(models.Manager):
    def get_queryset(self):
        return OtpRequestQuerySet(self.model, self._db)

    def is_valid(self, receiver, request, password):
        return self.get_queryset().is_valid(receiver, request, password)
    
    def generate(self, data):
        otp = self.model(channel=data['channel'], receiver=data['receiver'])
        otp.save(using=self._db)
        send_otp(otp)
        return otp


def generate_otp():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits, k=4)
    return  ''.join(digits)

class OTPRequest(models.Model):
    class OtpChannel(models.TextChoices):
        PHONE = 'phone',
        EMAIL = 'email',

    request_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    channel = models.CharField(max_length=10, choices=OtpChannel.choices, default=OtpChannel.PHONE)
    receiver = models.CharField(max_length=50)
    password = models.CharField(max_length=4, default=generate_otp)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    objects = OTPManager()


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
