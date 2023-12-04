from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Item

# class UserCreationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)
#     email = forms.EmailField(max_length=254, required=True)

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'picture', 'category', 'condition', 'starting_price', 'end_date', 'start_date']