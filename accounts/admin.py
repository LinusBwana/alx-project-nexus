from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Inline admin to display and edit the UserProfile on the same page as User
class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'Profile'
    verbose_name_plural = 'Profile'

# Custom admin for our custom User model
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline] # Attach the profile inline so User + Profile appear together

    # Adding your custom fields
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ['username', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
    # Make auto-generated fields read-only instead of editable
    readonly_fields = ["date_joined", "last_login"]


# Register the custom User admin so it replaces Django's default handling
admin.site.register(User, UserAdmin)