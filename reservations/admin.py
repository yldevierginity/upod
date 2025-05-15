from django.contrib import admin
from .models import ReservationDetails, ReservationRoomDetails, ReservationStatusLog, AttendeeList, Attendee
# Register your models here.

admin.site.register(ReservationDetails)
admin.site.register(ReservationRoomDetails)
admin.site.register(ReservationStatusLog)
admin.site.register(AttendeeList)
admin.site.register(Attendee)