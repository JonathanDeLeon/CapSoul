# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate, get_user_model
from django.core import serializers

from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from capsoul import tasks
from database.models import ExpiringToken

# Get the User Model
UserModel = get_user_model()

# Create your views here.
@api_view(['POST'])
@permission_classes((AllowAny, ))
def ajax_login(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
    except:
        return Response({'status':'Params not set'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({'status':'No user matches the given query'}, status=status.HTTP_404_NOT_FOUND)
    token = ExpiringToken.objects.get(user=user)
    if token.expired():
        token.delete()
        token = ExpiringToken.objects.create(user=user)
    response = Response({'status':'login successful','token':token.key, 'user':json.loads(serializers.serialize('json', [user, ]))}, status=status.HTTP_200_OK)
    # response.set_cookie('token_session', token.key)
    return response

@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        email = data['email']
    except:
        return Response({'status':'Params not set'}, status=status.HTTP_400_BAD_REQUEST)
    if UserModel.objects.filter(username=username).exists():
        return Response({'status':'User already exists'}, status=status.HTTP_404_NOT_FOUND)
    del data['username']
    del data['password']
    try:
        user = UserModel.objects.create_user(username, password, **data)
    except:
        return Response({'status':'There is an invalid keyword parameter'}, status=status.HTTP_400_BAD_REQUEST)
    token, created = ExpiringToken.objects.get_or_create(user=user)
    response = Response({'status':'User has successfully been created','token':token.key}, status=status.HTTP_201_CREATED)
    tasks.send_welcome_email.apply_async(args=[email], countdown=2)
    # response.set_cookie('token_session', token.key)
    return response

@api_view(['GET', 'POST'])
def ajax_logout(request):
    response = Response({'status':'Successfully logged out'}, status=status.HTTP_200_OK)
    response.delete_cookie('token_session')
    return response

@api_view(['GET'])
def verify(request):
    if request.user is AnonymousUser:
        return Response({'status':'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED, headers='WWW-Authenticate: Token')
    token = ExpiringToken.objects.get(user=request.user)
    if token.expired():
        token.delete()
        token = ExpiringToken.objects.create(user=request.user)
    return Response({'status':'token is verified','user':json.loads(serializers.serialize('json', [request.user, ]))}, status=status.HTTP_200_OK)

class ObtainExpiringAuthToken(ObtainAuthToken):
    """View enabling username/password exchange for expiring token"""
    model = ExpiringToken
    def post(self, request):
        try:
            data = json.loads(request.body)
        except:
            return Response({'status':'Params not set'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AuthTokenSerializer(data=data)
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()

