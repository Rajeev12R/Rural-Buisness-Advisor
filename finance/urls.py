from django.urls import path
from . import views

urlpatterns = [
    path(
        "business/<int:business_id>/new/",
        views.create_financial_plan,
        name="create_financial_plan",
    ),
    path(
        "plans/<int:plan_id>/",
        views.financial_plan_detail,
        name="financial_plan_detail",
    ),
]