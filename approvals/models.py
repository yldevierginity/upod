from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # safer than importing User directly, works with custom User models

class ApprovalAudit(models.Model):
    reservation = models.ForeignKey('reservations.ReservationDetails', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    status_choice = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reservation} - {self.status_choice} by {self.admin} at {self.timestamp}"
