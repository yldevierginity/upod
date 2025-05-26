from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from reservations.models import ReservationRoomDetails

# Create your views here.

@login_required
def index(request):
    user = request.user
    
    return render(request, 'userdashboard/index.html')

def logout_views(request):
    logout(request)
    response = HttpResponse()
    response['HX-Redirect'] = '/'
    return response

def render_dashboard(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')
    
    reservations = ReservationRoomDetails.objects.filter(reservation_detail__organizer=user)


    return render(request, 'dashboard/dashboard.html', {
        'user': user,
        'reservations': reservations,
    })
