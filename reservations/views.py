from django.shortcuts import render, redirect
from .forms import ReservationDetailsForm, ReservationRoomDetailsForm, ReservationStatusLogForm, AttendeeFormSet
from .models import ReservationDetails, ReservationRoomDetails, ReservationStatusLog, AttendeeList #only AttendeeList is actually used, may need to erase the others later
                                                                                                   #as they are already implicity called via the forms

# Create your views here.

# ReservationDetails holds ReservationRoomDetails and ReservationStatusLog
# ReservationRoomDetails holds AttendeeList
# It is safe to say that AttendeeList MUST BE SAVED FIRST, followed by ReservationRoomDetails and ReservationStatusLog in any order, then finally ReservationDetails
def create_reservation(request):

    if request.method == "POST":
        #Create form instances
        attendees_formset = AttendeeFormSet(request.POST)
        roomdetails_form = ReservationRoomDetailsForm(request.POST)
        status_form = ReservationStatusLogForm(request.POST)
        reservation_form = ReservationDetailsForm(request.POST)

        #form validation check
        if attendees_formset.is_valid() and roomdetails_form.is_valid() and status_form.is_valid() and reservation_form.is_valid():
            
            #start with AttendeeList and attendees first, contextualized via the formset
            attendee_list = AttendeeList.objects.create() #instantiate the list of attendees
            attendees_formset.instance = attendee_list #insert individual attendees managed by the formset into the instantiated list of attendees
            attendees_formset.save() #save the attendees within the formset to the database

            #attendee list has been created, save details within roomdetaills_form now along with inserting the attendee list we just made as foreign key
            room_details = roomdetails_form.save(commit=False) #instantiate roomdetails without saving first; attendee list hasn't been added yet
            room_details.attendee_list = attendee_list #attach recently saved attendees_formset now named attendee_list
            room_details.save()

            #save the status log as well
            status_log = status_form.save() #I don't know why we must instantiate the save into status_log, but might as well. It still saves it anyway

            #reservation details can now be saved with children to be attached
            reservation_details = reservation_form.save(commit=False)
            reservation_details.reservation_status_log = status_log
            reservation_details.reservation_room_details = room_details

            #I don't know the details of how users are going to be handled yet so I will comment this part for now
            # reservation_details.organizer = ??? definitely not request.user due to potential manually made user entity

            reservation_details.save()

            return redirect('reservation_success')
        
    else: #if the form hasn't submitted yet
        #initialize the forms
        attendees_formset = AttendeeFormSet()
        roomdetails_form = ReservationRoomDetailsForm()
        status_form = ReservationStatusLogForm()
        reservation_form = ReservationDetailsForm()

    return render(request, 'reservationpage_tobenamedproperlylater.html', {
        'attendees_formset': attendees_formset,
        'roomdetails_form': roomdetails_form,
        'status_form': status_form,
        'reservation_form': reservation_form
    })