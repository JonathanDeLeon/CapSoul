# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, Capsule, Media, Letter, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Capsule)
admin.site.register(Media)
admin.site.register(Letter)
admin.site.register(Comment)