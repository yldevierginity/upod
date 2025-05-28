from django.shortcuts import render, redirect
from .models import Room
from django.conf import settings

# Create your views here.
def show_selection(request):
    if request.user.is_authenticated:
        rooms = Room.objects.all()

        return render(request, 'rooms/roomselection.html', {'rooms': rooms})
    return redirect(settings.ACCOUNT_LOGOUT_REDIRECT_URL)
