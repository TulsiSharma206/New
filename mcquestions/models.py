from django.db import models
from django.utils import timezone
from user.models import User


class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    image = models.FileField(upload_to="studentimages")
    #coupan = models.CharField(max_length=127, blank=True, null=True)
    otp = models.CharField(max_length=17, blank=True, null=True)
    otp_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    varifed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "List Of Student"
        verbose_name_plural = "List Of Student"


class Mcquestions(models.Model):
    question = models.CharField(max_length=255)
    text1 = models.CharField(max_length=255)
    text2 = models.CharField(max_length=255)
    text3 = models.CharField(max_length=255)
    is_correct = models.CharField(max_length=255)

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = "MCQ Questions"
        verbose_name_plural = "MCQ Questions"


class StudentProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='StudentProgress')
    question = models.ForeignKey(Mcquestions, on_delete=models.CASCADE, related_name='Studentanswers')
    is_right = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Student Progress"
        verbose_name_plural = "Student Progress"



class StudentPercentage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='StudentPercentage')
    percentag = models.CharField(max_length=255, verbose_name='percentage')
    created_at = models.DateTimeField(auto_now_add=True)
    coupancode = models.CharField(max_length=255, verbose_name='coupan code')


class NumberOfQuestions(models.Model):
    multiplechoice = models.CharField(max_length=255, verbose_name='number of questions show in mcquestions')
    mock = models.CharField(max_length=255, verbose_name='number of questions show in mock')
    assement = models.CharField(max_length=255, verbose_name='number of questions show in assement')
    
    class Meta:
        verbose_name = "Number Of Questions"
        verbose_name_plural = "Number Of Questions"
