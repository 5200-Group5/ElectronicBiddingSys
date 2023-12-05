from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import UserRegisterForm



# Create your views here.

class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "user/register.html"
    success_url = reverse_lazy("user:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "user/login.html"


class UserLoginView(LoginView):
    template_name = "user/login.html"
