import os
from django.utils.timezone import now
from django.db import models
from django.core.exceptions import ValidationError #for the FileField part of ReservationRoomDetails
from django.conf import settings

#Imports to be added when existent

#from Upodusers app models import admin (not syntax correct yet)
#from Upodusers app models import upodusers (not syntax correct yet)
#from Upoduses.models import Admin, Upodusers | This is correct syntax, add when available

#from room app models import rooms (not syntax correct yet)
#from Room.models import Room | This is correct syntax, add when available


# Create your models here.
# note that currently, only Attendee is the child that has a field which holds a 'pointer' to its parent. It also seems to be the only one that cascades deletion properly

#Individual_Attendees
def validate_up_email(value):
    if not value.endswith('@up.edu.ph'):
        raise ValidationError("Email must end with @up.edu.ph")

class Attendee(models.Model):
    attendee_list = models.ForeignKey('AttendeeList', on_delete=models.CASCADE, related_name='listings')
    # user = models.ForeignKey('upodusers', on_delete=models.CASCADE) #commented this out for testing purposes, will use integer field for now
    # user = models.IntegerField() Change of plans, user has to be of an email field instead for easier error handling
    user = models.EmailField(validators=[validate_up_email])

    class Meta:
        unique_together = ('attendee_list', 'user')

    def __str__(self):
        return f"{self.user} in {self.attendee_list}"

#Attendee_List
class AttendeeList(models.Model):
    #Relationship to Reservation_Room_Details is handled in that class
    #Relationship to the multiple attendees are defined in that class
    #I made this to prevent many to many relationships
    pass

    def __str__(self):
        return f"Attendee List #{self.pk}; attached to {self.reservation_room_detail}"

#This is what the internet said on how to deal with FileFields. Will test it later
#===================================================================================
def validate_file_size(value):
    filesize = value.size
    limit_mb = 5
    if filesize > limit_mb * 1024 * 1024:
        raise ValidationError(f"File size should not exceed {limit_mb}MB")
    
def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')
    
def endorsement_upload_path(instance, filename):
    # Ensure a unique file name by using the reservation ID and current timestamp
    file_extension = os.path.splitext(filename)[1]
    return f'reservations/{now().strftime("%Y%m%d%H%M%S")}{file_extension}'
#===================================================================================

#Reservation_Room_Details
class ReservationRoomDetails(models.Model):
    cover_image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE) #this is supposed to get the value dynamically from rooms app
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    attendee_list = models.OneToOneField('AttendeeList', on_delete=models.CASCADE, related_name="reservation_room_detail")
    letter_of_endorsement = models.FileField(
        upload_to=endorsement_upload_path,
        validators=[validate_file_size, validate_file_extension]
    )
    event_name = models.CharField(max_length=20)
    event_description = models.CharField(max_length=255)

    @property
    def number_of_attendees(self): #this stands in for num of pax (I don't even know what pax is)
        return self.attendee_list.listings.count()
    
    def __str__(self):
        return f"{self.event_name} on {self.date} [{self.start_time}-{self.end_time}] in {self.room}"

#Reservation_Status_Log
class ReservationStatusLog(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('D', 'Denied'),
    ]

    # admin_in_charge = models.OneToOneField('admin', on_delete=models.SET_NULL, null=True, blank=True) # commented this out for testing purposes, will use integer field for now
    admin_in_charge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    time_stamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Status: {self.get_status_display()} by {self.admin_in_charge} at {self.time_stamp}"

#Reservation_Details
class ReservationDetails(models.Model):
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations", null=False, blank=False)
    reservation_room_details = models.OneToOneField('ReservationRoomDetails', on_delete=models.CASCADE, related_name="reservation_detail")
    reservation_status_log = models.OneToOneField('ReservationStatusLog', on_delete=models.CASCADE, related_name="reservation_detail")

    def __str__(self):
        return f"Reservation by: {self.organizer} | For: {self.reservation_room_details}"