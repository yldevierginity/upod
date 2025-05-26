from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'dashboard'

urlpatterns = [
    # path('', views.index, name='index'),
    path('accounts/logout/', LogoutView.as_view(), name="account_logout"),
    path('', views.render_dashboard, name='dashboardhome'),
    path('logout/user/', views.logout_views, name='logout_views'),
]
