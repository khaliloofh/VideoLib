import os
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.http import HttpResponse
from ranged_response import RangedFileResponse

def serve_media(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(file_path):
        return HttpResponse(status=404)
    return RangedFileResponse(request, open(file_path, 'rb'))


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve_media),
    ]