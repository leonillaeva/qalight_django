from django.contrib import admin

from . import models


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active", "date_joined")
    list_display_links = ("id", "email")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                )
            },
        ),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
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
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)


@admin.register(models.ActivateToken)
class ActivateTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "create_at")
    search_fields = ("user", "token")


@admin.register(models.AccessAPIToken)
class AccessAPITokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "create_at")
    search_fields = ("user", "token")


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "date_of_birth", "info")
    list_filter = ("user", "gender", "date_of_birth")
    search_fields = ("user", "gender")
