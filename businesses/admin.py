from django.contrib import admin
from .models import BusinessProfile


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "business_type",
        "village",
        "district",
        "available_capital",
        "owner",
    )

    list_filter = ("business_type", "state", "district")

    search_fields = (
        "business_name",
        "village",
        "district",
    )