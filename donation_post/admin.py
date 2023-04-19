from django.contrib import admin

from donation_post.models import DonationLog, DonationPost

@admin.register(DonationPost)
class DonationPostAdmin(admin.ModelAdmin):
    list_display = [ 'donation_for', 'id', 'amount', 'country', 'state', 'latitude', 'longitude', 'end_date', 'created_at', 'user', 'is_complete' ]


@admin.register(DonationLog)
class DonationLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'donation_post', 'donor', 'amount', 'created_at']

