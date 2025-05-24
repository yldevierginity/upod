from django.db import models

# Create your models here.
class Event(models.Model):
    reservationdetails = models.OneToOneField('reservations.ReservationDetails', on_delete=models.CASCADE, related_name='event')
    created_at = models.DateTimeField(auto_now_add=True)