"""capsoul URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import users
import capsules

from login import views as login

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^token-auth/', login.obtain_expiring_auth_token),
    url(r'^login/', login.ajax_login),
    url(r'^register/', login.register),
    url(r'^verify/', login.verify),
    url(r'^logout/', login.ajax_logout),
    url(r'^users/', include('users.urls')),
    url(r'^capsules/', include('capsules.urls')),
    url(r'^users', users.views.all_users),
    url(r'^capsules', capsules.views.all_capsules)
]
