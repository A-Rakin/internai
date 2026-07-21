from django.contrib import admin
from applications.models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'internship', 'status', 'ai_match_score', 'applied_at')
    list_filter = ('status',)
    search_fields = ('student__user__email', 'internship__title')
