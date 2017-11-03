# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from django.views.decorators.http import require_http_methods, require_POST

from rest_framework.authtoken.models import Token

# Get the User Model
UserModel = get_user_model()

# Create your views here.

@require_POST
def login(request, *args, **kwargs):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        response = JsonResponse({'result':'success','token':token.key})
        response.set_cookie('session', token.key)
    else:
        response =  JsonResponse({'result':'error'})
    return response

@require_POST
def register(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password, is_active=True)
    if user is not None:
        response = JsonResponse({'result':'error', 'description':'User already exists'})
    else:
        user = UserModel.objects.create_user(username, password)
        token, created = Token.objects.get_or_create(user=user)
        response = JsonResponse({'result':'success','description':'User has been created','token':token.key})
        response.set_cookie('session', token.key)
    return response

@require_http_methods(["GET", "POST"])
def logout(request):
    response = JsonResponse({'result':'Successfully logged out'})
    response.delete_cookie('session')
    return response

