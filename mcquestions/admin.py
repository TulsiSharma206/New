from django.contrib import admin
from .models import  Student, Mcquestions, StudentPercentage ,NumberOfQuestions , StudentProgress


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'varifed')
    fields = ['name', 'email', 'mobile','image','varifed']


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'is_right')

@admin.register(Mcquestions)
class McquestionsAdmin(admin.ModelAdmin):
    list_display = ('question', 'text1', 'text2', 'text3', 'is_correct')


@admin.register(StudentPercentage)
class StudentPercentageAdmin(admin.ModelAdmin):
    list_display = ('student', 'percentag', 'coupancode','created_at')


admin.site.register(NumberOfQuestions)
