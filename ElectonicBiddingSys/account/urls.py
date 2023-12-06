from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = "account"

urlpatterns = [
    path("", views.myview, name="account"),
    path("history", views.history, name="history"),
    path('create_report', views.create_report, name='create_report'),
    path('save_report', views.save_report, name='save_report'),
    path('create_payment', views.create_payment, name='create_payment'),
    path('save_payment', views.save_payment, name='save_payment'),
]

