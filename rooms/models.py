from django.db import models

class Room(models.Model):
    roomlabel = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.roomlabel


class Calendar(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name="calendar")

    def __str__(self):
        return f"{self.room.roomlabel}'s Calendar"


class DateEntry(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name="date_entries")
    date = models.DateField()

    class Meta:
        unique_together = ('calendar', 'date')

    def __str__(self):
        return f"{self.calendar.room.roomlabel} - {self.date}"


class TimeReserved(models.Model):
    date_entry = models.ForeignKey(DateEntry, on_delete=models.CASCADE, related_name="time_reservations")
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    event = models.OneToOneField('events.Event', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.date_entry} [{self.starting_time} - {self.ending_time}]"

