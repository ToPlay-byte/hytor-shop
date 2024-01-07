from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **other_fields):
        other_fields.setdefault("is_staff", False)
        other_fields.setdefault("is_superuser", False)
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **other_fields
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            **other_fields
        )
        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='Username', db_index=True, max_length=20,
        help_text='Enter your username', unique=True
    )
    first_name = models.CharField(verbose_name='First name', max_length=20, help_text='Enter your name', null=True)
    last_name = models.CharField(verbose_name='Last name', max_length=20, help_text='Enter your surname')
    email = models.EmailField(verbose_name='Email', help_text='Enter your email', unique=True)
    sex = models.CharField(
        verbose_name='Sex', max_length=6,
        choices=[('Female', 'Female'), ('Male', 'Male')], null=True
    )
    password = models.CharField(
        verbose_name='Password:', max_length=126,
        help_text='Enter your password'
    )
    date_joined = models.DateTimeField(verbose_name="date joined", default=timezone.now, editable=False)
    is_staff = models.BooleanField(verbose_name='Staff', default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(verbose_name='Superuser', default=False)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def short_name(self):
        return self.first_name

    def __str__(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)






