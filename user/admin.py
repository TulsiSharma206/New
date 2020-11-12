from django.contrib import admin
from .models import User, Otp , Consultation, Enroll, Batch, PaymentInfo, contactUS
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token

from django.contrib.auth.admin import UserAdmin 

admin.site.unregister(Group)
admin.site.unregister(Token)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    fields = ['email', 'name', 'is_staff', 'is_active', 'image', 'date_joined', 'contact', 'password']


admin.site.register(User, CustomUserAdmin)


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'number', 'course', 'day', 'time', 'is_verify')
    fields = ['email', 'name', 'number', 'course', 'day', 'time', 'is_verify']


@admin.register(Enroll)
class EnrollAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'number', 'course', 'is_verify')
    fields = ['email', 'name', 'number', 'course', 'is_verify']


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'started_at')
    fields = ['name', 'started_at']


@admin.register(PaymentInfo)
class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'paymentId','amount', 'created_at')


@admin.register(contactUS)
class contactUSAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'email', 'course', 'createat', 'is_verify')
    fields = ('name', 'number', 'email', 'course', 'createat', 'is_verify')


admin.site.register(Otp)