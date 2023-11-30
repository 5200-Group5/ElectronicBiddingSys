from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def save(self, commit=True):
        instance: User = super().save(commit=False)
        instance.first_name = self.cleaned_data["first_name"]
        instance.last_name = self.cleaned_data["last_name"]
        if commit:
            instance.save()

        return instance

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
