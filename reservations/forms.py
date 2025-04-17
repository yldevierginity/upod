from django import forms
from django.forms import inlineformset_factory
from .models import (
    ReservationDetails, ReservationRoomDetails, ReservationStatusLog, AttendeeList, Attendee
)

#The relatively 'normal' forms

class ReservationRoomDetailsForm(forms.ModelForm):
    class Meta:
        model = ReservationRoomDetails
        exclude = ['attendee_list'] #This is a foreign key entity that is not meant to have fields as django implicitly handles it based on the one to one
                                    #and one to many from Attendee and ReservationRoomDetails

class ReservationStatusLogForm(forms.ModelForm):
    class Meta:
        model = ReservationStatusLog

class ReservationDetailsForm(forms.ModelForm):
    class Meta:
        model = ReservationDetails


#The part of the forms that require dynamic adding of stuff; apparently requires formset

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        exclude = ['attendee_list'] #same reason as with ReservationRoomDetails; also, Django apparently has a builtin reverse query function so that's that

#If I understand properly, this allows AttendeeList to hold multiple values of Attendee given the parent child relationship they have.
AttendeeFormSet = inlineformset_factory(
    AttendeeList, Attendee, form=AttendeeForm, extra=1, can_delete=True
)
