# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.core import serializers

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

# Get the User Model
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from database.models import ExpiringToken

UserModel = get_user_model()

# Create your views here.
@require_POST
def ajax_login(request, *args, **kwargs):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, created = ExpiringToken.objects.get_or_create(user=user)
        response = JsonResponse({'result':'success','token':token.key, 'user':json.loads(serializers.serialize('json', [user, ]))})
        response.set_cookie('session', token.key)
    else:
        response =  JsonResponse({'result':'error'})
    return response

@require_POST
def register(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = authenticate(request, username=username, password=password, is_active=True)
    if user is not None:
        response = JsonResponse({'result':'error', 'description':'User already exists'})
    else:
        user = UserModel.objects.create_user(username, password)
        token, created = ExpiringToken.objects.get_or_create(user=user)
        response = JsonResponse({'result':'success','description':'User has been created','token':token.key})
        response.set_cookie('token_session', token.key)
    return response

@require_http_methods(["GET", "POST"])
def ajax_logout(request):
    logout(request)
    response = JsonResponse({'result':'Successfully logged out'})
    response.delete_cookie('token_session')
    return response

@require_GET
def verify(request):
    cookie = request.COOKIES.get('token_session')
    if cookie:
        # token, _ = ExpiringToken.objects.get_or_create(token=cookie)
        user = ExpiringToken.objects.get(key=cookie).user
        response = JsonResponse({'result':'success','user':json.loads(serializers.serialize('json', [user, ]))})
    else:
        response =  JsonResponse({'result':'error'})
    return response

class ObtainExpiringAuthToken(ObtainAuthToken):
    """View enabling username/password exchange for expiring token"""
    model = ExpiringToken
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            token, _ = ExpiringToken.objects.get_or_create(
                user=serializer.validated_data['user']
            )
            if token.expired():
                token.delete()
                token = ExpiringToken.objects.create(
                    user=serializer.validated_data['user']
                )
            data = {'token': token.key}
            return Response(data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()

