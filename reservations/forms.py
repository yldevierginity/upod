from django import forms
from django.forms import inlineformset_factory
from .models import (
    ReservationRoomDetails, AttendeeList, Attendee
)

#The relatively 'normal' forms

class ReservationRoomDetailsForm(forms.ModelForm):
    class Meta:
        model = ReservationRoomDetails
        exclude = ['attendee_list', 'room'] #This is a OneToOne related entity that is not meant to have fields as django implicitly handles it based on the one to one
                                    #and one to many from Attendee and ReservationRoomDetails

#Form for status log unnecessary as it only needs to be created during reservation submission then modified later via buttons by admin

#Form for rerservation details also unnecessary


#The part of the forms that require dynamic adding of stuff; apparently requires formset

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        exclude = ['attendee_list'] #same reason as with ReservationRoomDetails, but this time foreign key; also, Django apparently has a builtin reverse query function so that's that

#If I understand properly, this allows AttendeeList to hold multiple values of Attendee given the parent child relationship they have.
AttendeeFormSet = inlineformset_factory(
    AttendeeList, Attendee, form=AttendeeForm, extra=5, can_delete=True #later, the extra will be according to how much the maximum people of rooms will be in each room in a separate app
)
