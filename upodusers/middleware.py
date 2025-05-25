from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse("index")
        if request.user.is_authenticated and request.path in [login_url]:
            return redirect('dashboard')  # Replace 'home' with your desired URL name
        return self.get_response(request)

