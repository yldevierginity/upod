from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from reservations.models import ReservationRoomDetails
from .models import Event
from django.conf import settings

User = get_user_model()

def render_events(request):
    if not request.user.is_authenticated:
        return redirect(settings.ACCOUNT_LOGOUT_REDIRECT_URL)

    user = request.user
    email = user.email

    # Get reservations organized by user
    reservations = ReservationRoomDetails.objects.filter(
        reservation_detail__organizer=user
    )

    # Build reservation data with attendees resolved
    reservation_data_list = []
    for room_details in reservations:
        attendee_emails = room_details.attendee_list.listings.values_list('user', flat=True)
        attendees = list(User.objects.filter(email__in=attendee_emails))

        reservation_data_list.append({
            'reservation': room_details,
            'attendees': attendees,
        })

    # Get events user is attending (via attendee email)
    events = Event.objects.filter(
        reservationdetails__reservation_room_details__attendee_list__listings__user=email
    ).distinct()

    # Build event data with attendees fully resolved
    event_data_list = []
    for event in events:
        attendee_emails = event.reservationdetails.reservation_room_details.attendee_list.listings.values_list('user', flat=True)
        attendees = list(User.objects.filter(email__in=attendee_emails))

        event_data_list.append({
            'event': event,
            'attendees': attendees,
        })

    context = {
        'user': user,
        'reservation_data_list': reservation_data_list,
        'event_data_list': event_data_list,
    }

    return render(request, 'events/events.html', context)

