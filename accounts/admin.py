from django.contrib import admin
from accounts.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'id', 'first_name', 'last_name', 'role', 'is_active', 'is_deleted', 'created_at', 'modified_at', 'deleted_at'
    ]
