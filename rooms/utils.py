from rooms.models import Room, Calendar, DateEntry, TimeReserved

def time_conflict(room_id, date, start_time, end_time, current_event_id=None):
    """
    Returns True if there's a time conflict with existing approved Events (TimeReserved linked to Events).
    current_event_id can be passed to exclude the event itself (useful when editing).
    """
    try:
        date_entry = DateEntry.objects.get(calendar__room_id=room_id, date=date)
    except DateEntry.DoesNotExist:
        return False  # no reservations/events on this date yet

    # Filter TimeReserved entries that have linked Events (approved)
    time_reserved_qs = TimeReserved.objects.filter(
        date_entry=date_entry,
        event__isnull=False
    )
    
    if current_event_id:
        time_reserved_qs = time_reserved_qs.exclude(event_id=current_event_id)

    for reserved in time_reserved_qs:
        # Check for overlapping time ranges
        if start_time < reserved.ending_time and end_time > reserved.starting_time:
            return True  # conflict found

    return False  # no conflicts



def get_approved_time_blocks(room_id, date):
    """
    Returns TimeReserved entries for a given room and date that are confirmed (i.e., linked to an Event).
    """
    return (
        TimeReserved.objects.filter(
            date_entry__calendar__room_id=room_id,
            date_entry__date=date,
            event__isnull=False  # Assumes TimeReserved has OneToOneField to Event
        )
        .select_related('date_entry__calendar', 'event')
        .order_by('starting_time')
    )
