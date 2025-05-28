from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/logout/', LogoutView.as_view(), name="account_logout"),
    path('logout', views.logout_views, name='logout_views'),
]
