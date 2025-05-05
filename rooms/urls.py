from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    # URL pattern for the room app
    path('selection/', views.show_selection, name='room_selection'),
]