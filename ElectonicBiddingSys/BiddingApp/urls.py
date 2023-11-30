from django.urls import path
# from BiddingApp import views

# urlpatterns = [
#     path('register/', views.register, name='register'),
#     path('login/', views.sign_in, name='login'),
# ]

from . import views


app_name = "BiddingApp"

urlpatterns = [
    path("itemlist/", views.ItemFilterView.as_view(), name="item_list")
]