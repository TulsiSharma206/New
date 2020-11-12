from django.contrib import admin
from .models import TeacherProgre, Batches, StudentProgres


@admin.register(TeacherProgre)
class TeacherProgresAdmin(admin.ModelAdmin):
    list_display = ('batch' ,"student", "course", 'chapter', 'media', 'weight', 'partialcomplete', 'fullcomplete')
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Batches)
class BatchesAdmin(admin.ModelAdmin):
    list_display = ('name' ,"created_at", "end_at", 'complete')


@admin.register(StudentProgres)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "course", 'videolen', 'chapter', 'media', 'weight')

