from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    studentID = models.CharField(max_length=20, unique=True, blank=True, null=True)
    course_year = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
