from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from .models import Address, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "address_type", "default")
    list_filter = ("user", "address_type", "default")
    search_fields = ("user", "address_type", "default")
    ordering = ("user", "address_type", "default")
