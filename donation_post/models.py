from django.db import models

from django.utils import timezone
from django.db.models import Sum
from accounts.models import User

import datetime


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
    def is_expired(self):
        return datetime.datetime.now().date() > self.end_date

    # @property
    # def is_complete(self):
    #     donationList = self.donationlog_set.all()
    #     total = sum([item.amount for item in donationList])
    #     return total >= self.amount

    @property
    def is_complete(self):
        total_donations = self.donationlog_set.all().aggregate(total=Sum("amount"))
        total = total_donations['total'] or 0
        return int(total) >= int(self.amount)

    @property
    def donation(self):
        return self.donationlog_set.all()
    
    @property
    def received_amount(self):
        return sum([item.amount for item in self.donationlog_set.all()])

    @property
    def user_details(self):
        return self.user

    def __str__(self):
        return str(self.user.first_name + " - " + self.user.last_name)


class DonationLog(models.Model):
    donation_post = models.ForeignKey(DonationPost, verbose_name="Donation Post", on_delete=models.CASCADE)
    donor = models.ForeignKey(User, verbose_name="Donor", on_delete=models.CASCADE)
    amount = models.FloatField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    @property
    def donor_details(self):
        return self.user

    def __str__(self):
        return str(self.donation_post.donation_for + " - " + self.donor.first_name)

