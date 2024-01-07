from django import forms

from captcha.fields import CaptchaField

from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email:', widget=forms.EmailInput(attrs={
        'class': 'form__input',
        'placeholder': 'Email',
        'id': 'email'
    }))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={
        'class': 'form__input',
        'placeholder': 'Password',
        'id': 'Password'
    }))
    captcha = CaptchaField(label='Captcha')


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form__input',
        'id': 'email'
    }))


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='Password', max_length=16, min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'form__input',
        'placeholder': 'Password',
        'id': 'Password'
    }))
    password2 = forms.CharField(label='Repeat password', max_length=16, min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'form__input',
        'placeholder': 'Password',
        'id': 'Password'
    }))

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            return None
        else:
            return self.cleaned_data


class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'last_name', 'first_name', 'email', 'sex', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form__input',
                'placeholder': 'example@email.com',
                'id': 'email'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': 'Username',
                'id': 'username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': 'First_name',
                'id': 'first_name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': 'Last_name',
                'id': 'last_name'
            }),
            'sex': forms.Select(attrs={
                'class': 'form__input',
                'id': 'sex'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form__input',
                'placeholder': 'Password',
                'id': 'Password'
            })
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'last_name', 'first_name', 'email', 'sex']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form__input',
                'placeholder': 'example@email.com',
                'id': 'email'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': 'Username',
                'id': 'username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': 'First_name',
                'id': 'first_name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': 'Last_name',
                'id': 'last_name'
            }),
            'sex': forms.Select(attrs={
                'class': 'form__input',
                'id': 'sex'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form__input',
                'placeholder': 'Password',
                'id': 'Password'
            })
        }
