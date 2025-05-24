from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('events/', views.render_events, name='events'),
]
