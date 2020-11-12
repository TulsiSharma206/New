from rest_framework import serializers
from .models import User , Consultation, Enroll, Batch, contactUS


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['email', 'image', 'name','contact','age','profession','location','password']


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation 
        fields = ['name', 'email', 'number', 'course', 'day', 'time' ]


class EnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enroll 
        fields = ['name', 'email', 'number', 'course']


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch 
        fields = '__all__'


class contactUSSerializer(serializers.ModelSerializer):
    class Meta:
        model = contactUS
        fields = '__all__'

