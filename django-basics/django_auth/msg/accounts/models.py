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


# NOTE: The teacher's reasoning for placing `PermissionsMixin` after
# `AbstractBaseUser` (rather than vice versa) is because that's how he'd
# always seen this example used in the documentation. The course was
# originally created when Python was in version 1.9, so this pattern
# may be obsolete.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    display_name = models.CharField(max_length=140)
    bio = models.CharField(max_length=140, blank=True, default='')
    avatar = models.ImageField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # `objects` is the same attribute referenced in `User.objects.all()`
    objects = UserManager()

    # Specify what field will be used as the unique identifier for looking
    # someone up in the database.
    USERNAME_FIELD = 'email'
    # List of fields that will be prompted for when creating a user via
    # the `createsuperuser` management command.
    REQUIRED_FIELDS = ['display_name', 'username']

    def __str__(self):
        return '@{}'.format(self.username)

    def get_short_name(self):
        return self.display_name

    def get_long_name(self):
        return '{} (@{}'.format(self.display_name, self.username)
