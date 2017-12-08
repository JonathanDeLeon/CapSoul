# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse, HttpResponse, Http404
from capsoul import tasks
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from database.models import User


@api_view(['GET', 'POST'])
def all_users(request):
    if request.method == 'GET':
        all_users = User.objects.all().values('username', 'first_name', 'last_name')
        return JsonResponse({'users': list(all_users)}, status=status.HTTP_200_OK)
    else:
        fields = {}
        try:
            fields = json.loads(request.body)
        except ValueError:
            for field in request.POST:
                fields[field] = request.POST[field]
        fields['username'] = request.user.username
        current_user = User(**fields)
        current_user.save()
        current_user.photo = request.FILES['photo']
        current_user.save()
        return Response({"status": "profile updated"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def specific_user(request, uname):
    user = User.objects.filter(username=uname).values()
    if not user:
        return Response({"status": "No user matches the given query."}, status=status.HTTP_404_NOT_FOUND)
    return JsonResponse(list(user)[0], status=status.HTTP_200_OK)

@api_view(['GET'])
def get_photo(request, uname):
    user = User.objects.filter(username=uname).get() 
    if not user:
        return Response({"status": "No profile picture matches given query."}, status=404)
    filename = user.photo.name.split('/')[-1]
    response = HttpResponse(user.photo, content_type='image/*')
    response['Content-Disposition'] = 'attatchment; filename=%s' % filename
    return response