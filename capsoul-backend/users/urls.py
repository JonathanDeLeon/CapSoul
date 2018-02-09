from django.conf.urls import url
from django.contrib import admin

import users.views as views

urlpatterns = [
    url(r'^media/(.*)', views.get_photo),
    url(r'^(.*)', views.specific_user)
]