from django.shortcuts import render
from .models import Room

# Create your views here.
def show_selection(request):
    rooms = Room.objects.all()

    return render(request, 'rooms/roomselection.html', {'rooms': rooms})

