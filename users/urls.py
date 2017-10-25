from django.conf.urls import url
from django.contrib import admin

import users.views as views

urlpatterns = [
    url(r'^', views.all_users),
    url(r'^(.*)', views.specific_user),
]
