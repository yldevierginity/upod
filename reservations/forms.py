from django import forms
from .models import (
    ReservationRoomDetails, Attendee
)
from django.forms.widgets import DateInput, TimeInput
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

#The relatively 'normal' forms

class ReservationRoomDetailsForm(forms.ModelForm):
    class Meta:
        model = ReservationRoomDetails
        exclude = ['attendee_list', 'room'] #This is a OneToOne related entity that is not meant to have fields as django implicitly handles it based on the one to one
                                    #and one to many from Attendee and ReservationRoomDetails
        widgets = {
            'date': DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'start_time': TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'end_time': TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
        }

#Form for status log unnecessary as it only needs to be created during reservation submission then modified later via buttons by admin

class BaseAttendeeFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.current_user_email = kwargs.pop('current_user_email', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        emails = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                email = form.cleaned_data.get('user')
                if email == self.current_user_email:
                    raise ValidationError(f"The logged-in user's email '{email}' cannot be added as an attendee.")
                if email in emails:
                    raise ValidationError(f"Duplicate attendee email detected: {email}")
                emails.append(email)

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        exclude = ['attendee_list'] #same reason as with ReservationRoomDetails, but this time foreign key; also, Django apparently has a builtin reverse query function so that's that


