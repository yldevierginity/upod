"""
URL configuration for UPOD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Accounts
    path('accounts/', include('allauth.urls')),
    # Local Paths
    path('', include('upodusers.urls')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('rooms/', include('rooms.urls')),
    path('reservations/', include('reservations.urls')),
    path('events/', include('events.urls')),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'UPOD.views.handler404'
handler500 = 'UPOD.views.handler500'
handler403 = 'UPOD.views.handler403'
handler400 = 'UPOD.views.handler400'
