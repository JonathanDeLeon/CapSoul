# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from database.models import Capsule


@require_http_methods(["GET", "POST"])
def all_capsules(request):
    if request.method == 'GET':
        all_capsules = Capsule.objects.all().values('title', 'description', 'recipients')
        return JsonResponse({'capsules': list(all_capsules)}, status=200)
    else:
        return JsonResponse({"status": "resource created"}, status=200)


@require_http_methods(["GET", "POST"])
def specific_capsule(request, cid):
    if request.method == "GET":
        capsule = Capsule.objects.filter(cid=cid).values()
        return JsonResponse({'capsules': list(capsule)}, status=200)
    else:
        return JsonResponse({"status": "resource created"}, status=200)


@require_GET
def get_media(request, cid, mid):
    return JsonResponse({"owner": "rabery", "url": "http://lorempixel.com/400/400/cats/"},
                        status=200
                        )


@require_GET
def get_letters(request, cid, lid):
    return JsonResponse({"text": "Hey, I made this capsule for you! Hope you like it", "title": "Best Wishes",
                         "owner": "rabery"})


@require_POST
def add_media(request, cid):
    return JsonResponse({"status": "resource created"}, status=200)


@require_POST
def add_letters(request, cid):
    return JsonResponse({"status": "resource created"}, status=200)


@require_POST
def add_comments(request, cid):
    return JsonResponse({"status": "resource created"}, status=200)
