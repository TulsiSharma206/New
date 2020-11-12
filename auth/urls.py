from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
#from rest_framework_swagger.views import get_swagger_view


#schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    #path('', schema_view),
    path('', admin.site.urls),
    path('api/', include('user.urls')),
    path('course/', include('course.urls')),
    path('question/', include('mcquestions.urls')),
    path('progres/', include('progress.urls')),

    path('rest-auth/', include('rest_auth.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "ANG"
admin.site.site_title = "ANG Admin Portal"
admin.site.index_title = "ANG Portal"
