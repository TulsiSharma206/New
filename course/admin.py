from django.contrib import admin
from .models import Course, FileUpload, Purchase, assignments, Count, CurrentVideo , Chapter,  MockTest, AssignmentsTest,MockTestPercentage, AssignmentsPercentage , MockTestProgress,AssignmentsProgress, NumberofMock
# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "user", 'upload_date', 'status')
    search_fields = ("title__startswith", )
    
    
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("purchaseuser", "cours", 'status', 'date')
    #list_filter = ("purchaseuser", "cours")
    search_fields = ("purchaseuser__startswith", "cours__startswith")
    # def has_add_permission(self, request, obj=None):
    #     return False



#@admin.register(Count)
#class CountAdmin(admin.ModelAdmin):
#    list_display = ("user", 'mediafile', 'watch', 'is_complete')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("course", 'title','price', 'priceusd' ,'description')


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ("name", 'courses', 'chapter')
    # def has_add_permission(self, request, obj=None):
    #     return False

#admin.site.register(CurrentVideo)

@admin.register(NumberofMock)
class NumberofMockAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = ('cours', 'mock', 'question', 'text1', 'text2', 'text3', 'is_correct')


@admin.register(MockTestPercentage)
class MockPercentageAdmin(admin.ModelAdmin):
    list_display = ('cours','student', 'percentag', 'created_at')


@admin.register(MockTestProgress)
class MockTestProgressAdmin(admin.ModelAdmin):
    list_display = ('cours', 'mock', 'student', 'question', 'is_right')


@admin.register(AssignmentsProgress)
class AssignmentsProgressAdmin(admin.ModelAdmin):
    list_display = ('cours', 'chapter', 'student', 'question', 'is_right')


@admin.register(AssignmentsTest)
class AssignmentsTestAdmin(admin.ModelAdmin):
    list_display = ('cours', 'chapter', 'question', 'text1', 'text2', 'text3', 'is_correct')


@admin.register(AssignmentsPercentage)
class AssignmentsPercentageAdmin(admin.ModelAdmin):
    list_display = ('cours','chapter', 'student', 'percentag', 'created_at')

