from django.contrib import admin
from .models import OTP, UserProfile

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'otp_code', 'is_verified', 'created_at', 'expires_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at', 'expires_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_verified', 'created_at']
    list_filter = ['email_verified', 'created_at']
    search_fields = ['user__email', 'user__username']
