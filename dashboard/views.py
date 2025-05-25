from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth.models import User


@login_required
def index(request):
    # From django.contrib.auth.models.User
    user = request.user  

    name = user.get_full_name() or user.username
    email = user.email

    return render(request, 'dashboard/index.html', {
        'name': name,
        'email': email,
    })

def test_view(request):
    data = login_required.objects.all()
    return render(request, 'dashboard/index.html', {
        'data': data,
    })