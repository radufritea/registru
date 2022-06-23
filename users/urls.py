from django.urls import path, include
from . import views

app_name = "users"
urlpatterns = [
    path("", views.index, name="index"),
    path("employee_list/", views.employees, name="employees"),
    path("employee/<int:user_id>/", views.profile, name="profile"),
    path("edit_profile/<int:user_id>/", views.edit_profile, name="edit_profile"),
    path("", include("django.contrib.auth.urls")),
]
