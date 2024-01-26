from django import forms

from .models import *


class ReviewForm(forms.ModelForm):
    """Цей класс створює форму для відгуку"""

    class Meta:
        model = Review
        fields = '__all__'
