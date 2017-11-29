# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse, Http404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.core import serializers

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from database.models import ExpiringToken

# Get the User Model
UserModel = get_user_model()

# Create your views here.
@require_POST
def ajax_login(request, *args, **kwargs):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = authenticate(request, username=username, password=password)
    if user is None:
        raise Http404('No user matches the given query')
    login(request, user)
    token, created = ExpiringToken.objects.get_or_create(user=user)
    response = JsonResponse({'status':'login successful','token':token.key, 'user':json.loads(serializers.serialize('json', [user, ]))}, status=200)
    response.set_cookie('session', token.key)
    return response

@require_POST
def register(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = authenticate(request, username=username, password=password, is_active=True)
    if user is not None:
        raise Http404('User already exists')
    user = UserModel.objects.create_user(username, password)
    token, created = ExpiringToken.objects.get_or_create(user=user)
    response = JsonResponse({'status':'User has been successfully created','token':token.key}, status=200)
    response.set_cookie('token_session', token.key)
    return response

@require_http_methods(["GET", "POST"])
# @login_required(login_url='/auth-error/')
def ajax_logout(request):
    logout(request)
    response = JsonResponse({'status':'Successfully logged out'})
    response.delete_cookie('token_session')
    return response

@require_GET
# @login_required(login_url='/auth-error/')
def verify(request):
    cookie = request.COOKIES.get('token_session')
    if cookie is None:
        raise Http404('Invalid token')
    # token, _ = ExpiringToken.objects.get_or_create(token=cookie)
    user = ExpiringToken.objects.get(key=cookie).user
    response = JsonResponse({'status':'token is verified','user':json.loads(serializers.serialize('json', [user, ]))}, status=200)
    return response

@require_http_methods(["GET", "POST"])
def auth_error(request):
    raise Http404('User not authenticated. Login required.')

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

