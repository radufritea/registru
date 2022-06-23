from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import Http404

from .models import User
from .forms import UserForm


# Create your views here.
def index(request):
    return render(request, "index.html")


def employees(request):
    employees = User.objects.all().order_by("last_name")
    context = {"employees": employees}
    return render(request, "employee_list.html", context)


def profile(request, user_id):
    profile = User.objects.get(id=user_id)
    context = {"profile": profile}
    return render(request, "profile.html", context)


def edit_profile(request, user_id):
    profile = User.objects.get(id=user_id)
    if request.method == "POST":
        form = UserForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:profile", user_id=user_id)
        else:
            print(form.errors)
    else:
        form = UserForm(instance=profile)

    context = {"profile": profile, "form": form}
    return render(request, "edit_profile.html", context)
