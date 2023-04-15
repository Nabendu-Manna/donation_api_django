from django.contrib import admin

from donation_post.models import DonationPost

@admin.register(DonationPost)
class DonationPostAdmin(admin.ModelAdmin):
    list_display = [
        'donation_for', 'id', 'amount', 'country', 'state', 'latitude', 'longitude', 'end_date', 'created_at', 'user',
    ]
