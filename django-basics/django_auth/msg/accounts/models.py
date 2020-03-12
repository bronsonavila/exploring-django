from django.contrib.auth.models import (
    AbstractBaseUser, # All user models should be based on `AbstractBaseUser`.
    BaseUserManager, # Model manager that all user models use.
    PermissionsMixin, # Provides for user group permissions, etc.
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, display_name=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not display_name:
            display_name = username

        # `self.model()` is whatever model the manager is attached to.
        user = self.model(
            # Ensure all emails throughout the app are formatted the same.
            email=self.normalize_email(email),
            username=username,
            display_name=display_name,
        )
        # Handle password encryption and validation checks.
        user.set_password(password)
        user.save()
        return user

    # This is the method that is called when you run:
    # $ python manage.py createsuperuser
    def create_superuser(self, email, username, display_name, password):
        user = self.create_user(
            email,
            username,
            display_name=display_name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
