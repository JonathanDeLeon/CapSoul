# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from datetime import datetime
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from pytz import utc

from database.models import Capsule, User


@require_http_methods(["GET", "POST"])
def all_capsules(request):
    if request.method == 'GET':
        all_capsules = Capsule.objects.all().values('cid', 'unlocks_at', 'title', 'recipients', 'owner')
        return JsonResponse({'capsules': list(all_capsules)}, status=200)
    else:
        fields = json.loads(request.body)
        contributors = fields['contributors']
        del fields['contributors']
        recipients = fields['recipients']
        del fields['recipients']
        fields['owner'] = User.objects.get(username=request.user.username)

        capsule = Capsule(**fields)
        capsule.save()

        contribs = []
        for contributor in contributors:
            contribs.append(User.objects.get(username=contributor))
        capsule.contributors = contribs

        recips = []
        for recipient in recipients:
            recips.append(User.objects.get(username=recipient))
        capsule.recipients = recips

        capsule.save()
        return JsonResponse({"status": "resource with id created", "cid": capsule.cid}, status=200)


@require_http_methods(["GET", "POST"])
def specific_capsule(request, cid):
    if request.method == "GET":
        capsule = Capsule.objects.filter(cid=cid)
        if not capsule:
            raise Http404("No capsule matches the given query.")
        if capsule.get().unlocks_at > utc.localize(datetime.now()) and\
                capsule.get().owner.username != request.user.username and\
                request.user.username not in capsule.get().contributors.values('username'):
            return JsonResponse({"status": "Capsule is locked. Check back later!"}, status=401)
        if request.user.username not in capsule.get().recipients.values('username'):
            return JsonResponse({"status": "Not Authorized"}, status=401)
        return JsonResponse(list(capsule.values())[0], status=200)
    else:
        capsule = Capsule.objects.get(cid=cid)
        if capsule.owner.username != request.user.username:
            return JsonResponse({"status": "Not Authorized"}, status=401)
        fields = json.loads(request.body)
        contributors = fields['contributors']
        del fields['contributors']
        recipients = fields['recipients']
        del fields['recipients']
        fields['owner'] = User.objects.get(username=request.user.username)

        contribs = []
        for contributor in contributors:
            contribs.append(User.objects.get(username=contributor))
        capsule.contributors = contribs

        recips = []
        for recipient in recipients:
            recips.append(User.objects.get(username=recipient))
        capsule.recipients = recips

        for field in fields:
            capsule[field] = fields[field]
        capsule.save()
        return JsonResponse({"status": "resource with id created", "cid": capsule.cid}, status=200)


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
