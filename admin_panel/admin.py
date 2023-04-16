from django.contrib import admin

from admin_panel.models import HomePageLayout


@admin.register(HomePageLayout)
class HomePageLayoutAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'id', 'body_text', 'image', 'created_at'
    ]
