
from django.db import models
from django.contrib.auth.models import User


class BusinessProfile(models.Model):

    BUSINESS_TYPES = [
        ("grocery", "Grocery Shop"),
        ("dairy", "Dairy Farming"),
        ("agriculture", "Agriculture"),
        ("tailoring", "Tailoring"),
        ("handicraft", "Handicrafts"),
        ("other", "Other"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="business_profiles",
    )

    business_name = models.CharField(max_length=200)

    business_type = models.CharField(
        max_length=50,
        choices=BUSINESS_TYPES,
    )

    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default="Punjab")

    available_capital = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
