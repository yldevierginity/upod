from django.contrib import admin
from django.db import transaction
from reservations.models import ReservationDetails, ReservationRoomDetails, ReservationStatusLog, AttendeeList, Attendee
from rooms.models import Calendar, DateEntry, TimeReserved
from rooms.utils import get_conflicting_pending_reservations
from .models import ApprovalAudit
from events.models import Event
from django.utils import timezone
# Register your models here.

admin.site.register(ReservationDetails)
admin.site.register(ReservationRoomDetails)
# admin.site.register(ReservationStatusLog)
admin.site.register(AttendeeList)
admin.site.register(Attendee)
admin.site.register(ApprovalAudit)
admin.site.register(Event)

class ReservationStatusLogAdmin(admin.ModelAdmin):

    def get_model_perms(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='Admin_Group').exists():
            return super().get_model_perms(request)
        return {}

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        elif request.user.groups.filter(name='Admin_Group').exists():
            all_fields = [f.name for f in self.model._meta.fields]
            # Only allow editing 'special_field' (change this to your actual editable field name)
            return [f for f in all_fields if f != 'status']
        return [f.name for f in self.model._meta.fields]

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Admin_Group').exists()

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Admin_Group').exists()

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def save_model(self, request, obj, form, change):
        if change:
            original_obj = ReservationStatusLog.objects.get(pk=obj.pk)
            if original_obj.status != obj.status:
                obj.admin_in_charge = request.user
                obj.time_stamp = timezone.now()
                if obj.status == 'A':
                    try:
                        with transaction.atomic():
                            reservation = ReservationDetails.objects.select_for_update().get(pk=obj.reservation_detail.pk)

                            if not hasattr(reservation, 'event'):
                                event = Event.objects.create(
                                    reservationdetails=reservation,
                                    created_at=timezone.now()
                                )

                                room_detail = reservation.reservation_room_details
                                room = room_detail.room
                                calendar = Calendar.objects.get(room=room)
                                date_entry, _ = DateEntry.objects.get_or_create(
                                    calendar=calendar,
                                    date=room_detail.date
                                )

                                TimeReserved.objects.create(
                                    date_entry=date_entry,
                                    starting_time=room_detail.start_time,
                                    ending_time=room_detail.end_time,
                                    event=event
                                )

                                ApprovalAudit.objects.create(
                                    reservation=obj.reservation_detail, 
                                    admin=request.user,
                                    status_choice=obj.status,
                                    timestamp=timezone.now()
                                )

                                rivals = get_conflicting_pending_reservations(
                                    room=room_detail.room,
                                    date=room_detail.date,
                                    start=room_detail.start_time,
                                    end=room_detail.end_time,
                                    exclude_reservation_id=reservation.pk
                                )

                                for rival in rivals:
                                    status_log = ReservationStatusLog.objects.create(
                                        status='D',
                                        admin_in_charge=request.user,
                                        time_stamp=timezone.now()
                                    )
                                    rival.reservation_status_log = status_log
                                    rival.save()

                                    ApprovalAudit.objects.create(
                                        reservation=rival, 
                                        admin=request.user,
                                        status_choice='D',
                                        timestamp=timezone.now()
                                    )
                    except ReservationDetails.DoesNotExist:
                        pass

        super().save_model(request, obj, form, change)

admin.site.register(ReservationStatusLog, ReservationStatusLogAdmin)