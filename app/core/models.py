"""
Database models
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """Manager for users"""
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new users"""
        if not email: # if no email is provided
            raise ValueError('Users must have an email address') # raise an error
        user = self.model(email=self.normalize_email(email), **extra_fields) # create a new users model
        user.set_password(password) # set the password this uses hashing
        user.save(using=self._db) # save the users

        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True # is staff
        user.is_superuser = True # is superuser
        user.save(using=self._db) # save the users
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) # is users active
    is_staff = models.BooleanField(default=False) # is users staff

    objects = UserManager()

    USERNAME_FIELD = 'email' # email is the username field
