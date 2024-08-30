from django import forms

from .models import Customer, ShippingAddress


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput (attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
        }
        labels = {
            'first_name': 'Ваше имя',
            'last_name': 'Ваша фамилия'
        }


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'region', 'phone']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес'
            }),
            'city': forms.Select(attrs={
                'class': 'form-select'
            }),
            'region': forms.Select(attrs={
                'class': 'form-select'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер телефона',
                'type': 'tel'
            }),
        }
        labels = {
            'address': 'Ваш адрес',
            'city': 'Ваш город',
            'region': 'Ваш регион',
            'phone': 'Ваш номер телефона'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].widget.choices = [('', 'Выберите город')] + list(self.fields['city'].widget.choices)
        self.fields['city'].widget.choices.pop(1)

        self.fields['region'].widget.choices = [('', 'Выберите регион')] + list(self.fields['region'].widget.choices)
        self.fields['region'].widget.choices.pop(0)
        self.fields['region'].widget.choices.pop(0)