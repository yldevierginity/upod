from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .forms import ReservationRoomDetailsForm, AttendeeForm, BaseAttendeeFormSet
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
        AttendeeList, Attendee, form=AttendeeForm,
        formset=BaseAttendeeFormSet,
        extra=dynamic_extra, 
        can_delete=True #later, the extra will be according to how much the maximum people of rooms will be in each room in a separate app
    )

    if request.method == "POST":
        #Create form instances
        attendees_formset = AttendeeFormSet(request.POST, current_user_email=request.user.email)
        roomdetails_form = ReservationRoomDetailsForm(request.POST, request.FILES)
        roomdetails_form.instance.room = room #for schedule conflict purposes; actual room assignment to model is done within transaction.atomic block

        #form validation check
        if attendees_formset.is_valid() and roomdetails_form.is_valid():
            
            try:
                with transaction.atomic():
                    attendee_list = AttendeeList.objects.create()
                    attendees_formset.instance = attendee_list
                    attendees_formset.save()

                    room_details = roomdetails_form.save(commit=False)
                    room_details.room = room
                    room_details.attendee_list = attendee_list
                    room_details.save()

                    status_log = ReservationStatusLog.objects.create()

                    reservation_details = ReservationDetails.objects.create(
                        organizer=request.user,
                        reservation_status_log=status_log,
                        reservation_room_details=room_details,
                    )

                messages.success(request, "Reservation form creation saved successfully!")
                return redirect('reservation_success', reservation_details_id=reservation_details.id)

            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
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
        'endorsement_file': room_details.letter_of_endorsement.url if room_details.letter_of_endorsement else None,
    })