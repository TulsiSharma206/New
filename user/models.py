from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import datetime


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    image = models.FileField(upload_to="profileimage", blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    token = models.CharField(blank=True, max_length=255)
    contact = models.CharField(max_length=255, unique=True)
    age = models.IntegerField(blank=True,null=True)
    profession = models.CharField(max_length=255,blank=True,null=True)
    location = models.CharField(max_length=255,blank=True,null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class PaymentInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paymentId = models.CharField(max_length=10, blank=True, null=True)
    amount = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Payment Info'
        verbose_name_plural = 'Payment Info'
    
    def __str__(self):
        return self.paymentId


class Otp(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otpu = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(auto_now_add=True)



class Consultation(models.Model):
    name = models.CharField(max_length=127, blank=True, null=True)
    email = models.CharField(max_length=127, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    course = models.CharField(max_length=127, blank=True, null=True)
    day = models.CharField(max_length=127, blank=True, null=True)
    time = models.CharField(max_length=127, blank=True, null=True)
    otp = models.CharField(max_length=127, blank=True, null=True)
    is_verify = models.BooleanField(default=False)
    otpct = models.DateTimeField(default=timezone.now, blank=True, null=True)


class Enroll(models.Model):
    name = models.CharField(max_length=127, blank=True, null=True)
    email = models.CharField(max_length=127, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    course = models.CharField(max_length=127, blank=True, null=True)
    otp = models.CharField(max_length=127, blank=True, null=True)
    is_verify = models.BooleanField(default=False)
    otpet = models.DateTimeField(default=timezone.now, blank=True, null=True)

    class Meta:
        verbose_name = "Enroll"
        verbose_name_plural = "Enroll"


class Batch(models.Model):
    name = models.CharField(max_length=127, blank=True, null=True)
    started_at = models.DateField()

    class Meta:
        verbose_name = "Batches"
        verbose_name_plural = "Batches"


class contactUS(models.Model):
    name = models.CharField(max_length=127, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=127, blank=True, null=True)
    course = models.CharField(max_length=127, blank=True, null=True)
    otp = models.CharField(max_length=127, blank=True, null=True)
    createat = models.DateTimeField(default=timezone.now, blank=True, null=True)
    is_verify = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "contact Us"
        verbose_name_plural = "contact Us"
