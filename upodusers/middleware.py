from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redirect_from_paths = [
            reverse('index'),
            reverse('account_login'),
            reverse('account_signup'),
            reverse('account_reset_password'),
        ]
        dashboard_url = reverse('dashboard')  # name of your dashboard URL

        # Only redirect if the user is authenticated and trying to access login
        if request.user.is_authenticated and request.path in redirect_from_paths:
            return redirect(dashboard_url)

        return self.get_response(request)

