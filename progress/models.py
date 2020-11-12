from django.db import models
from user.models import User 
from course.models import Course, Chapter ,FileUpload


class StudentProgres(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    media = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
    videolen = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(max_length=127, blank=True, null=True)

    class Meta:
        verbose_name = "Student Progress"
        verbose_name_plural = "Student Progress"

class Batches(models.Model):
    name = models.CharField(max_length=127, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField()
    complete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Batches"
        verbose_name_plural = "Batches"


class TeacherProgre(models.Model):
    batch = models.ForeignKey(Batches, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    media = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
    weight = models.CharField(max_length=127, blank=True, null=True)
    partialcomplete = models.BooleanField(default=False)
    fullcomplete = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Teacher Progress"
        verbose_name_plural = "Teacher Progress"
