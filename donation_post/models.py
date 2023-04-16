from django.db import models

from django.utils import timezone
from accounts.models import User

class DonationPost(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    donation_for = models.CharField(max_length=300, default=None, blank=True, null=True)
    amount = models.FloatField(default=None, blank=True, null=True)
    country = models.CharField(max_length=300, default=None, blank=True, null=True)
    state = models.CharField(max_length=300, default=None, blank=True, null=True)
    address = models.CharField(max_length=300, default=None, blank=True, null=True)
    latitude = models.CharField(max_length=300, default=None, blank=True, null=True)
    longitude = models.CharField(max_length=300, default=None, blank=True, null=True)
    end_date = models.DateField(default=None)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def user_details(self):
        return self.user

    def __str__(self):
        return str(self.user.first_name + " - " + self.user.last_name)


