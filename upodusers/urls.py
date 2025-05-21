from django.urls import path
from . import views

# Custom URL imports

urlpatterns = [
    # This is the app default index view url
    path('', views.index, name='index'),
    # This path is used when resetting password so that it does not redirect to the allauth default login template
    path('/', views.index, name='root'),
    path('logout', views.logout_view, name='logout'),
]
