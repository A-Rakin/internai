from django.contrib import admin
from documents.models import Document, ActivityLog

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'doc_type', 'file_size', 'uploaded_at')
    list_filter = ('doc_type',)
    search_fields = ('title', 'user__email')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'ip_address', 'created_at')
    list_filter = ('action',)
    search_fields = ('user__email', 'description')
