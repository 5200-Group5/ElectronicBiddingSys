from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = "account"

urlpatterns = [
    path("", views.myview, name="account"),
    path("history", views.history, name="history"),

]

