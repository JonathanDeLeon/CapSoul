
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length = 30, primary_key = True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    birthdate = models.DateField()
    photo = models.FileField()
    email = models.EmailField()
    phone = models.IntegerField() 
    location = models.TextField()

    def __str__(self):
        return self.user_name


class Capsule(models.Model):
    cid = models.AutoField(primary_key = True)
    unlocks_at = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    contributors = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    recipients = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
    title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title