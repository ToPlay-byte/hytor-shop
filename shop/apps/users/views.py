from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, RedirectView, UpdateView, TemplateView
from django.http import JsonResponse
from .forms import *
from .models import *


class LoginView(FormView):
    """Цей клас відповідає за представлення сторінки авторизації"""

    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('company:Home')

    def form_valid(self, form):

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        if user:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)

        return render(self.request, 'users/login.html', context={
            'error': 'Don`t correct email or password.',
            'form': LoginForm
        })


class SignUpView(FormView):
    """Цей клас відповідає за представлення сторінки реєстрації"""

    template_name = 'users/signup.html'
    form_class = SignUpForm
    form_class.fields = ['username', 'last_name', 'first_name', 'email', 'sex', 'password']
    success_url = reverse_lazy('company:Home')

    def form_valid(self, form):

        data = form.cleaned_data
        email = data.pop('email')
        password = data.pop('password')
        CustomUser.objects.create_user(email=email, password=password, **data)

        return super(SignUpView, self).form_valid(form)


class LogoutView(RedirectView):
    """Цей клас представлення відповідає, щоб користувач міг вийти зі свого облікового запису """

    pattern_name = 'company:Home'
    
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class ProfileView(UpdateView):
    """Цей клас представлення відповідає за сторінку з даними о користувачі"""

    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:Profile')

    def get_object(self, queryset=None):

        username = self.request.user.username
        user = get_object_or_404(CustomUser, username=username)

        return user

    def get_initial(self):

        user = self.get_object()
        initial = {
            'username': user.username,
            'last_name': user.last_name,
            'first_name': user.first_name,
            'email': user.email,
            'sex': user.sex
        }

        return initial


class SendingEmailSuccessfullyView(TemplateView):
    """Цей класс відповідає за класс за відображення сторінки, після успішного відправлення електронного листа на пошту"""

    template_name = 'users/reset_password/success.html'


class AjaxSignUpViews(FormView):
    """Цей клас представляє змогу дізнатися про помилки в формі за допомогою ajax"""

    form_class = SignUpForm
    template_name = 'users/signup.html'

    def form_invalid(self, form):

        response = {}

        for field, error in form.errors.items():
            response[field] = error

        return JsonResponse({'response': response, 'result': 'Error'})
