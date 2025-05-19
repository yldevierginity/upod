from django.urls import path
from . import views

# Custom URL imports

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_view, name='logout'),
]
