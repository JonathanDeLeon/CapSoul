# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from database.models import User


@api_view(['GET', 'POST'])
def all_users(request):
    if request.method == 'GET':
        all_users = User.objects.all().values('username', 'first_name', 'last_name')
        return JsonResponse({'users': list(all_users)}, status=200)
    else:
        fields = json.loads(request.body)
        fields['username'] = request.user.username
        current_user = User(**fields)
        current_user.save()
        return Response({"status": "resource created"}, status=200)


@api_view(['GET'])
def specific_user(request, uname):
    user = User.objects.filter(username=uname).values()
    if not user:
        return Response({"status": "No user matches the given query.", status=404)
    return JsonResponse(list(user)[0], status=200)
