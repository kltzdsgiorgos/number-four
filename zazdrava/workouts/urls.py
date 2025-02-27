from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "workouts"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("upload/", views.upload_workout, name="upload_workout"),
    path("upload/", views.upload_workout, name="upload"),
    path("workout/<int:workout_id>/", views.view_workout, name="view_workout"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="workouts:login"),
        name="logout",
    ),
]
