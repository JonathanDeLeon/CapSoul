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
        return JsonResponse({"status": "profile updated"}, status=200)


@api_view(['GET'])
def specific_user(request, uname):
    user = User.objects.filter(username=uname).values()
    if not user:
        return JsonResponse({"status": "No user matches the given query."}, status=404)
    return JsonResponse(list(user)[0], status=200)

@api_view(['GET'])
def get_photo(request, uname):
    user_pic = User.objects.filter(username=uname).get('photo') 
    if not user_pic:
        return Response({"status": "No profile picture matches given query."}, status=404)
    filename = user_pic.name.split('/')[-1]
    response = HttpResponse(user_pic, content_type='image/*')
    response['Content-Disposition'] = 'attatchment; filename=%s' % filename
    return response