from django.conf.urls import url
from django.contrib import admin

import capsules.views as views

urlpatterns = [
    url(r'^media/(.*)', views.get_media),
    url(r'^letters/(.*)', views.get_letters),
    url(r'^(.*)/media', views.add_media),
    url(r'^(.*)/letters', views.add_letters),
    url(r'^(.*)/comments', views.add_comments),
    url(r'^(.*)', views.specific_capsule),
    url(r'^', views.all_capsules)
]
