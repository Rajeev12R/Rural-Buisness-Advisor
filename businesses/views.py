
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import BusinessProfileForm
from .models import BusinessProfile


def home(request):
    return render(request, "businesses/home.html")


@login_required
def create_business(request):
    if request.method == "POST":
        form = BusinessProfileForm(request.POST)

        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()

            return redirect("dashboard")
    else:
        form = BusinessProfileForm()

    return render(
        request,
        "businesses/business_form.html",
        {"form": form},
    )


@login_required
def dashboard(request):
    businesses = (
        BusinessProfile.objects
        .filter(owner=request.user)
        .prefetch_related("financial_plans")
        .order_by("-created_at")
    )

    return render(
        request,
        "businesses/dashboard.html",
        {"businesses": businesses},
    )