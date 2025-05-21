from django import forms
from .models import (
    ReservationRoomDetails, Attendee
)
from django.forms.widgets import DateInput, TimeInput
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rooms.utils import time_conflict

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

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # The form does NOT have room in the fields, so expect it to be set on the instance externally (in the view)
        room = self.instance.room if self.instance and self.instance.room else None

        if not room:
            raise ValidationError("Room must be assigned to the reservation before validation.")

        if date and start_time and end_time:
            if time_conflict(room.id, date, start_time, end_time):
                raise ValidationError("The selected time conflicts with an existing reservation for this room.")

        return cleaned_data

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

    def clean_user(self):
        email = self.cleaned_data.get('user')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user with this email exists.")
        return email


