from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError #for the FileField part of ReservationRoomDetails

#Imports to be added when existent

#from Upodusers app models import admin (not syntax correct yet)
#from Upodusers app models import upodusers (not syntax correct yet)
#from Upoduses.models import Admin, Upodusers | This is correct syntax, add when available

#from room app models import rooms (not syntax correct yet)
#from Room.models import Room | This is correct syntax, add when available


# Create your models here.

#Individual_Attendees
class Attendee(models.Model):
    attendee_list = models.ForeignKey('AttendeeList', on_delete=models.CASCADE, related_name='listings')
    # user = models.ForeignKey('upodusers', on_delete=models.CASCADE) #commented this out for testing purposes, will use integer field for now
    user = models.IntegerField()

    class Meta:
        unique_together = ('attendee_list', 'user')

#Attendee_List
class AttendeeList(models.Model):
    #Relationship to Reservation_Room_Details is handled in that class
    #Relationship to the multiple attendees are defined in that class
    #I made this to prevent many to many relationships
    pass

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
#===================================================================================

#Reservation_Room_Details
class ReservationRoomDetails(models.Model):
    # room = models.OneToOneField('room', on_delete=models.CASCADE) #commented this out for testing purposes, will use integer field for now
    room = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    attendee_list = models.OneToOneField('AttendeeList', on_delete=models.CASCADE)
    # letter_of_endorsement = models.FileField(
    #     upload_to='', #will have to figure out how to use upload_to later, internet says something like '<name>/%Y/%m/%d/' to make a folder for each letters per date. I don't even know if that's secure
    #                   #may need authentication/gatekeeping related decorators, but this is on the reservation side of things rather than actual stuff. Will need to learn more about this
    #     validators=[validate_file_size, validate_file_extension]
    #     ) 
    # commented this out for testing purposes, will use integer field for now
    letter_of_endorsement = models.IntegerField()
    event_name = models.CharField(max_length=20)
    event_description = models.CharField(max_length=255)

    @property
    def number_of_attendees(self): #this stands in for num of pax (I don't even know what pax is)
        return self.attendee_list.listings.count()

#Reservation_Status_Log
class ReservationStatusLog(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('D', 'Denied'),
    ]

    # admin_in_charge = models.OneToOneField('admin', on_delete=models.SET_NULL, null=True, blank=True) # commented this out for testing purposes, will use integer field for now
    admin_in_charge = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    time_stamp = models.DateTimeField(null=True, blank=True)

#Reservation_Details
class ReservationDetails(models.Model):
    # organizer = models.OneToOneField('upodusers', on_delete=models.CASCADE) # commented this out for testing purposes, will use integer field for now
    organizer = models.IntegerField(null=True, blank=True)
    reservation_room_details = models.OneToOneField('ReservationRoomDetails', on_delete=models.CASCADE)
    reservation_status_log = models.OneToOneField('ReservationStatusLog', on_delete=models.CASCADE)