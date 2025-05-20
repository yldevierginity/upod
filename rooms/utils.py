from .models import Room, Calendar, DateEntry, TimeReserved

def time_conflict(room_id, date, start_time, end_time, current_reservation_id=None):
    """
    Returns True if there's a time conflict in the room's schedule, False otherwise.
    Optionally pass the ID of a reservation being edited to ignore it in the check.
    """
    try:
        date_entry = DateEntry.objects.get(calendar__room_id=room_id, date=date)
    except DateEntry.DoesNotExist:
        return False  # No existing reservations yet for this room on this date

    reservations = TimeReserved.objects.filter(date_entry=date_entry)

    if current_reservation_id:
        reservations = reservations.exclude(id=current_reservation_id)

    for res in reservations:
        if start_time < res.ending_time and end_time > res.starting_time:
            return True  # Conflict exists

    return False  # No conflict


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
