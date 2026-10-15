
from django import forms
from .models import BusinessProfile


class BusinessProfileForm(forms.ModelForm):

    class Meta:
        model = BusinessProfile
        fields = [
            "business_name",
            "business_type",
            "village",
            "district",
            "state",
            "available_capital",
        ]

        widgets = {
            "business_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "business_type": forms.Select(
                attrs={"class": "form-control"}
            ),
            "village": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "district": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "available_capital": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                }
            ),
        }

    def clean_available_capital(self):
        capital = self.cleaned_data["available_capital"]

        if capital < 0:
            raise forms.ValidationError(
                "Available capital cannot be negative."
            )

        return capital
