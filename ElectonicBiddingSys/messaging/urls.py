from django.urls import path, include
from . import views

app_name = 'messaging'

urlpatterns = [
    path('send_message/<str:username>/', views.send_message, name='send_message'),
    path('view_message/', views.view_message, name='view_message'),
]