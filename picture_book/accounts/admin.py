from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import PasswordResetToken, Family, Invitation

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff', 'created_at', 'update_at')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff')
    
admin.site.register(User, UserAdmin)

class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'used', 'created_at')
    search_fields = ('user__email', 'token')
    
admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)


class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'update_at')
    search_fields = ('id',)
    
admin.site.register(Family, FamilyAdmin)


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('invite_token', 'family_id', 'user_id', 'used', 'expiry_date', 'created_at', 'update_at')
    search_fields = ('invite_token',)
    
admin.site.register(Invitation, InvitationAdmin)