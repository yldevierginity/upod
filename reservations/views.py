from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationRoomDetailsForm, AttendeeForm
from .models import ReservationDetails, ReservationStatusLog, AttendeeList, Attendee, ReservationRoomDetails
from rooms.models import Room
from django.contrib import messages
from django.forms import inlineformset_factory

# Create your views here.

# ReservationDetails holds ReservationRoomDetails and ReservationStatusLog
# ReservationRoomDetails holds AttendeeList
# It is safe to say that AttendeeList MUST BE SAVED FIRST, followed by ReservationRoomDetails and ReservationStatusLog in any order, then finally ReservationDetails
def create_reservation(request, room_id):

    room = get_object_or_404(Room, id=room_id)

    dynamic_extra = room.capacity if hasattr(room, 'capacity') else 1

    #If I understand properly, this allows AttendeeList to hold multiple values of Attendee given the parent child relationship they have.
    AttendeeFormSet = inlineformset_factory(
        AttendeeList, Attendee, form=AttendeeForm, extra=dynamic_extra, can_delete=True #later, the extra will be according to how much the maximum people of rooms will be in each room in a separate app
    )

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
            room_details.room = room
            room_details.attendee_list = attendee_list #attach recently saved attendees_formset now named attendee_list
            room_details.save()

            # #instantiate status log
            status_log = ReservationStatusLog.objects.create() #I don't know why we must instantiate the save into status_log, but might as well. It still saves it anyway
                                                               #every field in this is either intentionally defaulted as null or defaulted as a certain value, no need to save

            # #reservation details can now be saved with children to be attached

            # #I don't know the details of how users are going to be handled yet so I will comment this part for now
            #organizer = ??? definitely not request.user due to potential manually made user entity
            reservation_details = ReservationDetails.objects.create(
                reservation_status_log=status_log,
                reservation_room_details=room_details,
                #organizer=organizer, #handled later when user has been finalized
            )            
            messages.success(request, "Reservation form creation saved successfully!")
            return redirect('reservation_success',
                            reservation_details_id=reservation_details.id) #checks app's url patterns to see if there is a name 'reservation_success'; this does not go directly to function reservation_success
        else:
            messages.error(request, "There was an error with the form. Please try again.")
            return render(request, 'reservations/reservation.html', {
                'attendees_formset': attendees_formset,
                'roomdetails_form': roomdetails_form,
                'room': room,
            })

        
    else: #if the form hasn't submitted yet
        #initialize the forms
        attendees_formset = AttendeeFormSet()
        roomdetails_form = ReservationRoomDetailsForm()

    return render(request, 'reservations/reservation.html', {
        'attendees_formset': attendees_formset,
        'roomdetails_form': roomdetails_form,
        'room': room,
    })

def reservation_success(request, reservation_details_id):

    reservation_details = get_object_or_404(ReservationDetails, id=reservation_details_id)
    room_details = reservation_details.reservation_room_details
    status_log = reservation_details.reservation_status_log

    #This is for showing the currently submitted attendee_list
    #------------------------------------------------------------------
    # Retrieve the attendee list based on the passed attendee_list_id
    attendee_list = room_details.attendee_list
    # Fetch all AttendeeList instances
    attendees = attendee_list.listings.all()
    #------------------------------------------------------------------

    #This is for showing all the attendeelist and their respective attendees
    #------------------------------------------------------------------
    # attendees_per_attendee = []
    # for list_instance in attendee_lists:
    #     attendees = list_instance.listings.all()

    #     attendee_list_info = {
    #         'attendee_list_id': list_instance.id,
    #         'attendees': []
    #     }

    #     for attendee in attendees:
    #         attendee_list_info['attendees'].append({
    #             'attendee_id': attendee.id,
    #             'user': attendee.user
    #         })

    #     attendees_per_attendee.append(attendee_list_info)
    #-----------------------------------------------------------------------
    
    # Render the reservation success page, passing the attendee list
    # print("Status log debug:", status_log.id, status_log.status, status_log.time_stamp)

    return render(request, 'reservations/reservation_success.html', {
        'reservation_details': reservation_details,
        'room_details': room_details,
        'status_log': status_log,
        'attendees': attendees,
        # 'attendeees_per_attendee': attendees_per_attendee,
    })