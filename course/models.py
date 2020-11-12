from django.db import models
from user.models import User
from multiselectfield import MultiSelectField
import datetime
from mcquestions.models import Mcquestions


# Create your models here.


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=127, blank=True, null=True)
    sub_title = models.CharField(max_length=127, blank=True, null=True)
    # category = MultiSelectField(choices=COURSE_CATEGORY_TYPES,max_choices=5)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
    image = models.FileField(upload_to="courseimage")
    price = models.CharField(max_length=127, blank=True, null=True)
    priceusd = models.CharField(max_length=127, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class assignments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cours = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.FileField(upload_to="assigment")
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

 
class Chapter(models.Model):
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.CharField(max_length=127, blank=True, null=True)
    priceusd = models.CharField(max_length=127, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class FileUpload(models.Model):
    name = models.CharField(blank=True, null=True, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE , blank=True, null=True)
    chapter = models.ForeignKey(Chapter, related_name='videos', on_delete=models.CASCADE , blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE , blank=True, null=True)
    image = models.FileField(upload_to="image", blank=True, null=True)
    uploadfile = models.FileField(upload_to="video")
    url = models.CharField(max_length=127, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "List Of File Uploaded"
        verbose_name_plural = "List Of File Uploaded"


class Count(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # cours = models.ForeignKey(Course, on_delete=models.CASCADE)
    mediafile = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
    watch = models.IntegerField(default=0)
    vtime = models.CharField(blank=True, null=True, max_length=50)
    is_complete = models.BooleanField(default=False)


class CurrentVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coures = models.ForeignKey(Course, on_delete=models.CASCADE)
    # cours = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    currenv = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
    time = models.CharField(max_length=127, blank=True, null=True)


class Purchase(models.Model):
    purchaseuser = models.ForeignKey(User, on_delete=models.CASCADE)
    cours = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    media = models.ManyToManyField(FileUpload, related_name="multipleVideo" )
    status = models.BooleanField(default=True)
    date = models.DateField(auto_now=True)
    #end_date = models.DateField()
    
    class Meta:
        verbose_name = "Course Purchase"
        verbose_name_plural = "Course Purchase"

class NumberofMock(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 
    class Meta:
        verbose_name = "Number Of Mock"
        verbose_name_plural = "Number Of Mock"


class MockTest(models.Model):
    cours = models.ForeignKey(Course,blank=True, null=True, on_delete=models.CASCADE)
    #chapter = models.ForeignKey(Chapter,blank=True, null=True, on_delete=models.CASCADE)
    mock = models.ForeignKey(NumberofMock,blank=True, null=True, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    text1 = models.CharField(max_length=255)
    text2 = models.CharField(max_length=255)
    text3 = models.CharField(max_length=255)
    is_correct = models.CharField(max_length=255)

    def __str__(self):
        return self.question
    class Meta:
        verbose_name = "Mock Test"
        verbose_name_plural = "Mock Test"


class MockTestProgress(models.Model):
    cours = models.ForeignKey(Course, on_delete=models.CASCADE,blank=True, null=True, related_name='MockTestsCourse')
    mock = models.ForeignKey(NumberofMock,blank=True, null=True, on_delete=models.CASCADE)
    #chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,blank=True, null=True, related_name='MockTestsChapter')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='MockTestsProgress')
    question = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='MockTestanswers')
    is_right = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Mock Test Progress"
        verbose_name_plural = "Mock Test Progress"



class MockTestPercentage(models.Model):
    cours = models.ForeignKey(Course, blank=True, null=True,on_delete=models.CASCADE, related_name='MockTest')
    #chapter = models.ForeignKey(Chapter, blank=True, null=True,on_delete=models.CASCADE, related_name='Mockchapter')
    mock = models.ForeignKey(NumberofMock,blank=True, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='MockTestsPercentage')
    percentag = models.CharField(max_length=255, verbose_name='mockpercentage')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Mock Test Percentage"
        verbose_name_plural = "Mock Test Percentage"


class AssignmentsTest(models.Model):
    cours = models.ForeignKey(Course,blank=True, null=True, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter,blank=True, null=True, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    text1 = models.CharField(max_length=255)
    text2 = models.CharField(max_length=255)
    text3 = models.CharField(max_length=255)
    is_correct = models.CharField(max_length=255)
    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessment"


class AssignmentsProgress(models.Model):
    cours = models.ForeignKey(Course, on_delete=models.CASCADE,blank=True, null=True, related_name='Assignmentcourse')
    chapter = models.ForeignKey(Chapter,blank=True, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='AssignmentProgress')
    question = models.ForeignKey(AssignmentsTest, on_delete=models.CASCADE, related_name='Assignmentsanswers')
    is_right = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Assessment Progress"
        verbose_name_plural = "Assessment Progress"


class AssignmentsPercentage(models.Model):
    cours = models.ForeignKey(Course, on_delete=models.CASCADE,blank=True, null=True, related_name='Assignmentchapter')
    chapter = models.ForeignKey(Chapter,blank=True, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='AssignmentPercentage')
    percentag = models.CharField(max_length=255, verbose_name='Assignmentpercentage')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Assessment Percentage"
        verbose_name_plural = "Assessment Percentage"
