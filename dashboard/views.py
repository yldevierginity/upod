from django.shortcuts import render, redirect
from reservations.models import ReservationRoomDetails

# Create your views here.
def render_dashboard(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')
    
    reservations = ReservationRoomDetails.objects.filter(reservation_detail__organizer=user)


    return render(request, 'dashboard/dashboard.html', {
        'user': user,
        'reservations': reservations,
    })