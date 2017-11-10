# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET


@require_http_methods(["GET", "POST"])
def all_users(request):
    if request.method == 'GET':
        return JsonResponse({"users": [{"user_name": "rabery", "first": "Ryan", "last": "Rabello"},
                                       {"user_name": "beavet", "first": "Ethan", "last": "Beaver"}
                                       ]},
                            status=200
                            )
    else:
        return JsonResponse({"status": "resource created"}, status=200)


@require_GET
def specific_user(request, user_name):
    return JsonResponse({"user_name": "rabery", "first": "Ryan", "last": "Rabello",
                                    "birthdate": "1992-09-02", "photo": "ryan.jpg",
                                    "email": "ryan.rabello@gmail.com", "phone": "212-479-7990",
                                    "location": "Walla Walla, WA"},
                        status=200
                        )
