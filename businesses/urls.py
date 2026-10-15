from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "business/new/",
        views.create_business,
        name="create_business",
    ),
]