# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST


@require_http_methods(["GET", "POST"])
def all_capsules(request):
    if request.method == 'GET':
        return JsonResponse({"capsules": [{"cid": "1", "unlock_at": "2017-12-10T14:30Z", "owner": "rabery",
                                           "recipient": "beavet", "title": "Winter Surprise"},
                                          {"cid": "2", "unlock_at": "2017-12-10T14:30Z", "owner": "beavet",
                                           "recipient": "rabery", "title": "Anniversary"},
                                          {"cid": "3", "unlock_at": "2017-11-2T14:30Z", "owner": "beavet",
                                           "recipient": "rabery", "title": "Software Engineering"}
                                          ]
                             },
                            status=200
                            )
    else:
        return JsonResponse({"status": "resource created"}, status=200)


@require_http_methods(["GET", "POST"])
def specific_capsule(request, cid):
    if request.method == "GET":
        return JsonResponse({"cid": "1", "unlock_at": "2017-12-10T14:30Z", "owner": "rabery", "recipient": "beavet",
                             "title": "Winter Surprise", "contributors": ["fennma", "delejo"],
                             "description": "A capsule that Ryan made for Ethan for being such a good ASWWU employee",
                             "media": ["1", "2"], "letters": ["1", "3"],
                             "comments": [{"owner": "rabery", "text": "test comment"}]},
                            status=200
                            )
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
