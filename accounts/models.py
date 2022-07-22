from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        """
          Create and save a user with the given username, email, and password.
          """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
     """
     Custom User model with email as username field
     """
     username = None

     email = models.EmailField(_('email address'),
                               blank=True,
                               unique=True)

     objects = CustomUserManager()

     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = []
