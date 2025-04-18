from django.shortcuts import render, redirect
from .forms import ReservationRoomDetailsForm, AttendeeFormSet
from .models import ReservationDetails, ReservationStatusLog, AttendeeList
from django.template.loader import render_to_string
from django.http import HttpResponse

# Create your views here.

def add_attendee_form(request):
    formset = AttendeeFormSet()
    form = formset.empty_form
    form_html = render_to_string("partials/attendee_form.html", {'form': form})
    return HttpResponse(form_html)

# ReservationDetails holds ReservationRoomDetails and ReservationStatusLog
# ReservationRoomDetails holds AttendeeList
# It is safe to say that AttendeeList MUST BE SAVED FIRST, followed by ReservationRoomDetails and ReservationStatusLog in any order, then finally ReservationDetails
def create_reservation(request):

    if request.method == "POST":
        #Create form instances
        attendees_formset = AttendeeFormSet(request.POST)
        roomdetails_form = ReservationRoomDetailsForm(request.POST)

        #form validation check
        if attendees_formset.is_valid() and roomdetails_form.is_valid():
            
            #start with AttendeeList and attendees first, contextualized via the formset
            attendee_list = AttendeeList.objects.create() #instantiate the list of attendees
            attendees_formset.instance = attendee_list #insert individual attendees managed by the formset into the instantiated list of attendees
            attendees_formset.save() #save the attendees within the formset to the database

            #attendee list has been created, save details within roomdetaills_form now along with inserting the attendee list we just made as foreign key
            room_details = roomdetails_form.save(commit=False) #instantiate roomdetails without saving first; attendee list hasn't been added yet
            room_details.attendee_list = attendee_list #attach recently saved attendees_formset now named attendee_list
            room_details.save()

            #instantiate status log
            status_log = ReservationStatusLog.objects.create() #I don't know why we must instantiate the save into status_log, but might as well. It still saves it anyway
                                                               #every field in this is either intentionally defaulted as null or defaulted as a certain value, no need to save

            #reservation details can now be saved with children to be attached

            #I don't know the details of how users are going to be handled yet so I will comment this part for now
            #organizer = ??? definitely not request.user due to potential manually made user entity
            reservation_details = ReservationDetails.objects.create(
                reservation_status_log=status_log,
                reservation_room_details=room_details,
                #organizer=organizer, #handled later when user has been finalized
            )            

            return redirect('reservation_success')
        
    else: #if the form hasn't submitted yet
        #initialize the forms
        attendees_formset = AttendeeFormSet()
        roomdetails_form = ReservationRoomDetailsForm()

    return render(request, 'reservation.html', {
        'attendees_formset': attendees_formset,
        'roomdetails_form': roomdetails_form,
    })