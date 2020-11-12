from django.urls import path
from .views import coursecomplete ,chaptercount, mediacount ,teacherprogres, batchlist , teacherlist, Teacherpro, teacherprogresdata, stprogress  , studentprogress             #progress


urlpatterns = [
    path('coursecount/', coursecomplete,name="courses completed"),
    path('chaptercount/<pk>/', chaptercount,name="chapter count"),
    path('mediacount/<pk>/', mediacount,name="media count"),
    path('teacherprogres/', teacherprogres,name="media count"),
    path('batchlist/', batchlist,name="list batch"),
    path('teacherlist/', teacherlist,name="list Teacher"),

    path("teacherpro/", Teacherpro, name="Teacher Progress html"),
    path("teacherprogresdata/", teacherprogresdata, name="Teacher Progress data"),
    
    #path('<pk>/', progress,name="Student Progress"),   

    path("studentprogres/", stprogress, name="Student Progress stored video wise"),
    path("studentpro/", studentprogress, name="Student all Progress"),
]
