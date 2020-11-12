from rest_framework import serializers
from .models import Course, FileUpload, Purchase, assignments, Count , CurrentVideo, Chapter


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'sub_title', 'image', 'description', 'price'] 


class FileUploadSerializer(serializers.ModelSerializer): #Hyperlinked
    # owner = serializers.SlugRelatedField(read_only=True,slug_field='id')
    class Meta:
        model = FileUpload
        # fields = ['id' ,'image', 'uploadfile', 'url']
        fields = ['id','owner' ,'image', 'uploadfile', 'url']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['purchaseuser', ]


class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Count
        fields = ['watch',]

class CurrentVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentVideo
        fields =  '__all__' #['user', 'mediafile', 'time']

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields =  '__all__' #['user', 'mediafile', 'time']


# class assignmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = assignments
#         fields = ['cours', 'assignment', 'text']
