from django.urls import path, reverse_lazy
from django.contrib.auth import views as reset
from django.contrib.auth.decorators import login_required

from . import views


app_name = 'users'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='Log in'),
    path('sign_up', views.SignUpView.as_view(), name='Sign up'),
    path(
        'reset_password',
        reset.PasswordResetView.as_view(
            template_name='users/reset_password/send_mail.html',
            email_template_name='users/reset_password/mail.html',
            success_url=reverse_lazy('users:Success'),
            from_email='oleksandr.hnylosyr@gmail.com'
        ),
        name='Reset password'
    ),
    path('success', views.SendingEmailSuccessfullyView.as_view(), name='Success'),
    path(
        'change_password/<uidb64>/<token>/',
        reset.PasswordResetConfirmView.as_view(
            template_name='users/reset_password/change_password.html', success_url=reverse_lazy('users:Log in')
        ),
        name='password_reset_confirm'
    ),
    path('logout/', views.LogoutView.as_view(), name='Log out'),
    path('profile', login_required(views.ProfileView.as_view()), name='Profile'),
    path('ajax_sign_up', views.AjaxSignUpViews.as_view()),
]
