from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = "user"

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
