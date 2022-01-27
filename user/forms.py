from django import forms
from django.forms import TextInput
from django.forms import Form
from django.forms.widgets import EmailInput
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy


class SellerRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=gettext_lazy("رمز عبور"), strip=False,
        widget=forms.PasswordInput(attrs={'class': "input100",
                                          'placeholder': "رمز عبور"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label=gettext_lazy("تایید رمز عبور"), strip=False,
        widget=forms.PasswordInput(attrs={'class': "input100",
                                          'placeholder': "تایید رمز عبور"}),

        help_text=gettext_lazy("برای تایید همان رمز عبور قبلی را وارد کنید."),
    )

    class Meta:
        model = User
        fields = ("phone", "username", "email", "password1", "password2")
        widgets = {
            'phone': TextInput(
                attrs={'class': "input100", 'placeholder': "شماره همراه"}),

            'username': TextInput(
                attrs={'class': "input100", 'placeholder': "نام کاربری"}),

            'email': EmailInput(attrs={'class': "input100", 'placeholder': "ایمیل"}),
        }

    def save(self, commit=True):
        user = super(SellerRegisterForm, self).save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.is_seller = True
        if commit:
            user.save()
        return user


class SellerLoginForm(Form):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': "input100", 'type': "text", 'name': "email", 'placeholder': "شماره همراه"}))

    password = forms.CharField(strip=False,
                               widget=forms.PasswordInput(
                                   attrs={'class': "input100", 'type': "password", 'name': "pass",
                                          'placeholder': "رمز عبور"}))
