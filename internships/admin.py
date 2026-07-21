from django.contrib import admin
from internships.models import InternshipCategory, Internship

@admin.register(InternshipCategory)
class InternshipCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'internship_type', 'status', 'is_approved', 'created_at')
    list_filter = ('status', 'is_approved', 'internship_type', 'category')
    search_fields = ('title', 'company__company_name', 'requirements')
