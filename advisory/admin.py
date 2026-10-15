from django.contrib import admin
from .models import AdvisoryReport


@admin.register(AdvisoryReport)
class AdvisoryReportAdmin(admin.ModelAdmin):
    list_display = ("financial_plan", "created_at", "updated_at")
    search_fields = ("financial_plan__business__business_name", "advisory_summary")
