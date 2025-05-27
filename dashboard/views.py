from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from reservations.models import ReservationRoomDetails
from django.conf import settings

# Create your views here.

@login_required
def index(request):
    user = request.user
    
    return render(request, 'userdashboard/index.html')

def logout_views(request):
    logout(request)

    if request.headers.get("HX-Request"):
        response = HttpResponse()
        response['HX-Redirect'] = settings.ACCOUNT_LOGOUT_REDIRECT_URL
        return response
    return redirect(settings.ACCOUNT_LOGOUT_REDIRECT_URL)

def render_dashboard(request):
    user = request.user

    if not user.is_authenticated:
        return redirect(settings.ACCOUNT_LOGOUT_REDIRECT_URL)
    
    reservations = ReservationRoomDetails.objects.filter(reservation_detail__organizer=user)


    return render(request, 'dashboard/dashboard.html', {
        'user': user,
        'reservations': reservations,
    })

def about_us(request):
    return render (request, 'dashboard/about.html')

def profile(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'dashboard/profile.html')
    return redirect(settings.ACCOUNT_LOGOUT_REDIRECT_URL)