from django.contrib import admin
from interviews.models import Interview

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'interview_type', 'mode', 'scheduled_at', 'outcome')
    list_filter = ('interview_type', 'mode', 'outcome')
    search_fields = ('application__student__user__email', 'interviewer_name')
