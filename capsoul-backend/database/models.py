# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.authtoken.models import Token

def _upload_path(instance,filename):
    return instance.get_upload_path(filename)

# Create your models here.
class UserManager(BaseUserManager):
    """
    Custom manager for User
    """
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    User with the same behaviour as Django's default User
    Attributes inherited from superclass:
        * password
        * last_login
        * is_superuser
    """
    username = models.CharField(max_length=30, primary_key=True, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(blank=True, upload_to=_upload_path)
    email = models.EmailField()
    phone = models.IntegerField(null=True, blank=True)
    location = models.TextField()
    date_joined = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField('verified', default=False)

    # Requirements for custom user
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_upload_path(self, filename):
        filename = str(self.username)
        return "media/"+filename

    def __str__(self):
        return self.username

    # Below 3 methods are required for custom django user
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


lifespan = timedelta(7)
class ExpiringToken(Token):
    """Extend Token to add an expired method"""
    class Meta(object):
        """This model is treated as a proxy model"""
        proxy = True

    def expired(self):
        now = timezone.now()
        if self.created < now - lifespan:
            return True
        return False


class Media(models.Model):
    mid = models.AutoField(primary_key=True)
    file = models.FileField(upload_to=_upload_path)
    capsule = models.ForeignKey('Capsule', related_name='media_capsule', null = True)
    owner = models.ForeignKey('User', related_name='media_owner')
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.mid)

    def get_upload_path(self, filename):
        filename = str(self.mid)
        return "media/"+filename


class Letter(models.Model):
    lid = models.AutoField(primary_key=True)
    title = models.CharField(default='', max_length=255)
    text = models.TextField(default='')
    owner = models.ForeignKey('User', related_name='letter_owner')
    capsule = models.ForeignKey('Capsule', related_name='cid_of_letter')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.lid)


class Capsule(models.Model):
    cid = models.AutoField(primary_key=True)
    unlocks_at = models.DateTimeField()
    owner = models.ForeignKey('User', related_name='capsule_owner')
    contributors = models.ManyToManyField('User', related_name='capsule_contributors')
    recipients = models.ManyToManyField('User', related_name='capsule_recipients')
    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    media = models.ManyToManyField('Media', related_name='media', blank=True)
    letter = models.ManyToManyField('Letter', related_name='letters', blank=True)
    date_created = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cid)


class Comment(models.Model):
    comid = models.AutoField(primary_key=True)
    title = models.CharField(default='', max_length=255)
    text = models.TextField(default='')
    owner = models.ForeignKey('User', related_name='comment_owner')
    capsule = models.ForeignKey('Capsule', related_name='comment_capsule')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.comid)