from django.urls import path, include
from django.contrib import admin
# from BiddingApp import views

# urlpatterns = [
#     path('register/', views.register, name='register'),
#     path('login/', views.sign_in, name='login'),
# ]

from . import views


app_name = "BiddingApp"

urlpatterns = [
    path("itemlist/", views.ItemFilterView.as_view(), name="item_list"),
    path('', views.bidding_page, name='bidding_page'),
    path('item_detail/<int:item_id>/', views.item_detail, name='item_detail'),
    path('place_bid/<int:item_id>/', views.place_bid, name='place_bid'),
    path("chatbot/", views.chatbot, name="chatbot"),
    path('create_item/', views.create_item, name='create_item'),
    path('save_item/', views.save_item, name='save_item'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('messaging/', include('messaging.urls', namespace='messaging')), 
]