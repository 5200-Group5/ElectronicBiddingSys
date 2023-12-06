from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ReportedIssue, transaction

# class UserCreationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)
#     email = forms.EmailField(max_length=254, required=True)

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ReportForm(forms.ModelForm):
    class Meta:
        model = ReportedIssue
        fields = ['message']

class PayForm(forms.ModelForm):
    class Meta:
        model = transaction
        fields = ['transaction_type','transaction_status']
