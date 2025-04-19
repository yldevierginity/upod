from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for the reservation success page
    path('create/', views.create_reservation, name='create_reservation'),
    path('success/<int:attendee_list_id>/', views.reservation_success, name='reservation_success'),
]
