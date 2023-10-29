# accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class Image(models.Model):
    image = models.ImageField(upload_to='profile_images/')

class Interest(models.Model):
    name = models.CharField(max_length=255)

class RejectedCards(models.Model):
    user=models.IntegerField()

class LikedCards(models.Model):
    user=models.IntegerField()

class LikedYou(models.Model):
    user=models.IntegerField()

class Matches(models.Model):
    user=models.IntegerField()

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True)
    interest = models.ManyToManyField(Interest, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    about = models.TextField(blank=True)
    latitude = models.CharField(max_length=255, blank=True)
    longitude = models.CharField(max_length=255, blank=True)
    image=models.ManyToManyField(Image, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    rejected=models.ManyToManyField(RejectedCards)
    liked=models.ManyToManyField(LikedCards)
    likedyou=models.ManyToManyField(LikedYou)
    matches=models.ManyToManyField(Matches)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


