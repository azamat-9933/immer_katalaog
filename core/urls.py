from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirect to the admin login page if no URL matches
    path('', lambda request: redirect('admin/', permanent=True)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)