from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts import models


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('name', 'sex', 'birth_date', 'phone_number', 'is_admin')

    def clean_password2(self):
        # Validates whether the two password inputs are the same.
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Saves the user instance with a hashed password.
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    # Read-only field for user password
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = ('name', 'sex', 'birth_date', 'phone_number', 'password', 'is_admin')

    def clean_password(self):
        return self.initial["password"]
