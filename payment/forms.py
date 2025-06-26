from django import forms
from .models import Order
from django_recaptcha.fields import ReCaptchaField

class OrderForm(forms.ModelForm):
    captcha = ReCaptchaField()
    
    class Meta:
        model = Order
        fields = ['email', 'phone_number', 'address']

        widgets = {
            'phone_number': forms.TextInput(attrs={
                'placeholder': '+216 .....',
                'pattern': r'^\+216\d{8}$',
                'title': 'Enter a valid Tunisian phone number (e.g. +21612345678)',
                'required': True,
            }),
        }
