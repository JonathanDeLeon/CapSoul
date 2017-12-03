# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods, require_GET
from capsoul import tasks
from django.db import models
from database.models import User


@require_http_methods(["GET", "POST"])
def all_users(request):
    if request.method == 'GET':
        all_users = User.objects.all().values('username', 'first_name', 'last_name')
        return JsonResponse({'users': list(all_users)}, status=200)
    else:
        fields = json.loads(request.body)
        fields['username'] = request.user.username
        current_user = User(**fields)
        current_user.save()
        email = fields['email']
        tasks.send_welcome_email.apply_async(args=[email], countdown=2)
        return JsonResponse({"status": "resource created"}, status=200)


@require_GET
def specific_user(request, uname):
    user = User.objects.filter(username=uname).values()
    if not user:
        raise Http404("No user matches the given query.")
    return JsonResponse(list(user)[0], status=200)
