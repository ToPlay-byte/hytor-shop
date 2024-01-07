from django import forms

from .models import Contacts


class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = '__all__'

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'contacts__input',
                'id': 'name',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.TextInput(attrs={
                'class': 'contacts__input',
                'id': 'email',
                'placeholder': 'Enter your email'
            })
        }
