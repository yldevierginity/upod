from django.shortcuts import render

# Create your views here.
def render_dashboard(request):
    return render(request, 'dashboard/dashboard.html')