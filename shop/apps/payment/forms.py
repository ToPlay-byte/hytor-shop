from django import forms

from .models import *


class OrderForm(forms.ModelForm):
    """Форма для створення заказу"""

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email']

        widgets = {field: forms.TextInput(attrs={
                'class': 'orders__input',
            })
            for field in fields
        }

