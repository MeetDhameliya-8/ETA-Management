
from django.contrib import admin
from .models import (
    User, NewJoineProfile, InternProfile,
    EmployeeProfile, HrProfile, ManagerProfile, OwnerProfile
)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin




@admin.register(User)
class UserAdmin(BaseUserAdmin):
    
    list_display = ["email", "phone", "role", "is_active", "is_admin",'is_staff']
    list_filter = ["role", "is_active", "is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password", "role"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "phone", "technology", "Experience"]}),
        ("Permissions", {"fields": ["is_active", "is_staff", "is_admin", "is_superuser"]}),
    ]
    add_fieldsets = [
        (None, {
            "classes": ["wide"],
            "fields": ["email", "phone", "role", "password1", "password2"],
        }),
    ]
    search_fields = ["email", "phone"]
    ordering = ["email"]


@admin.register(NewJoineProfile)
class NewJoineProfileAdmin(admin.ModelAdmin):
    list_display = ["FullName", "user", "created_at", "updated_at"]
    search_fields = ["FullName", "user__email"]


@admin.register(InternProfile)
class InternProfileAdmin(admin.ModelAdmin):
    list_display = ["FullName", "user", "Assigner", "Part_of_Project", "created_at"]
    search_fields = ["FullName", "user__email"]


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "Project", "Assigner", "salary"]
    search_fields = ["user__email", "Project"]


@admin.register(HrProfile)
class HrProfileAdmin(admin.ModelAdmin):
    list_display = ["FullName", "user", "department", "employees_under"]
    search_fields = ["FullName", "user__email"]


@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ["FullName", "user", "department", "Team"]
    search_fields = ["FullName", "user__email"]


@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ["FullName", "Experience"]
    search_fields = ["FullName"]


