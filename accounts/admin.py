"""
============================================================
Accounts Admin - Django Admin Registration
============================================================
Register all account-related models in Django Admin
for easy management through the admin interface.
============================================================
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser, StudentProfile, CompanyProfile, SupervisorProfile


class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser model."""
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'is_email_verified')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('InternAI Fields', {
            'fields': ('role', 'phone', 'avatar', 'is_email_verified'),
        }),
    )


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'department', 'education_level', 'gpa')
    search_fields = ('user__email', 'user__first_name', 'university')
    list_filter = ('education_level', 'gender')


class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'industry', 'company_size', 'is_verified')
    search_fields = ('company_name', 'user__email')
    list_filter = ('industry', 'is_verified', 'company_size')


class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'department', 'designation', 'max_students')
    search_fields = ('user__email', 'user__first_name', 'university')
    list_filter = ('designation',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(SupervisorProfile, SupervisorProfileAdmin)
