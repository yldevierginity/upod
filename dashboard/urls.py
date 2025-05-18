from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.render_dashboard, name='dashboard'),
]
