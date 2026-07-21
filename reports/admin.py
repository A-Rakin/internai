from django.contrib import admin
from reports.models import WeeklyReport, Evaluation

@admin.register(WeeklyReport)
class WeeklyReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'internship', 'week_number', 'status', 'score', 'submitted_at')
    list_filter = ('status', 'week_number')
    search_fields = ('student__user__email', 'title')

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('student', 'supervisor', 'internship', 'overall_score', 'is_final', 'created_at')
    list_filter = ('is_final',)
    search_fields = ('student__user__email', 'supervisor__user__email')
