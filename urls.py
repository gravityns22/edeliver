"""edeliver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, re_path, include
from .views import display_meta, contact_page, register, user_login, home_page, upload_file, upload_csv


urlpatterns = [
    re_path(r'^batch-geocode/$', upload_csv, name='batch-geocode'),
    re_path(r'^$', home_page),
    re_path(r'^login/$', user_login),
    re_path(r'^register/$', register),
	path('contact/', contact_page),
	path('meta/', display_meta),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
