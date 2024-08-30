from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile


# User -> Базовая модель в Django. Для пользователя, логин, пароль, is_staff,

# UserCreationForm -> Форма, которая создает пользователя без привилегий,
# с заданным логином и паролем


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        # привязываем модель User
        model = User
        # указываем какие поля выводить
        fields = ['username', 'password1', 'password2']


# AuthenticationForm -> Базовый класс для аутентификации пользователя

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['username', 'password']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'first_name', 'last_name']
        widgets = {
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваша фамилия'
            })
        }
        labels = {
            'profile_image': 'Аватарка',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
