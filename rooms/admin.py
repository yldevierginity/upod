from django.contrib import admin
from .models import Room, Calendar, DateEntry, TimeReserved
# Register your models here.

admin.site.register(Room)
admin.site.register(Calendar)
admin.site.register(DateEntry)
admin.site.register(TimeReserved)