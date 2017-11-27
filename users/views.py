# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET

from database.models import User


@require_http_methods(["GET", "POST"])
def all_users(request):
    if request.method == 'GET':
        all_users = User.objects.all().values('username', 'first_name', 'last_name')
        return JsonResponse({'users': list(all_users)}, status=200)
    else:
        fields = json.loads(request.body)
        fields['username'] = request.user.user_name
        current_user = User(**fields)
        current_user.save()
        return JsonResponse({"status": "resource created"}, status=200)


@require_GET
def specific_user(request, uname):
    user = User.objects.filter(username=uname).values()
    return JsonResponse({'users': list(user)}, status=200)
