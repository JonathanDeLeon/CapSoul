# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from datetime import datetime
from django.http import JsonResponse, HttpResponse, Http404
from pytz import utc

from rest_framework.decorators import api_view
from rest_framework.response import Response

import os, capsoul.settings
from database.models import Capsule, User, Media, Letter, Comment


@api_view(['GET', 'POST'])
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
        return Response({"status": "resource created", "cid": capsule.cid}, status=200)


@api_view(['GET', 'POST'])
def specific_capsule(request, cid):
    if request.method == "GET":
        capsule = Capsule.objects.filter(cid=cid)
        if not capsule:
            raise Http404("No capsule matches the given query.")
        authorized = check_authorized(cid, request.user.username, 'view')
        if isinstance(authorized, JsonResponse):
            return authorized
        try:
            media = Media.objects.filter(capsule=capsule.get())
        except:
            media = []
        all_media = []
        for m in media:
            all_media.append(m.mid)
            media_dir = capsoul.settings.MEDIA_ROOT+'media/'+str(m.mid)
            if os.path.exists(media_dir) is False:
                del all_media[-1]
        temp_list = list(capsule.values())[0]
        temp_list['media'] = all_media

        try:
            letters = Letter.objects.filter(capsule=capsule.get()).values('lid')
        except:
            letters = []
        all_letters = []
        for l in letters:
            all_letters.append(l["lid"])
        temp_list['letters'] = all_letters

        try:
            comments = Comment.objects.filter(capsule=capsule.get()).values('title', 'text', 'owner', 'comid', 'owner')
        except:
            comments = []
        all_comments = []
        for c in comments:
            all_comments.append(c)
        temp_list['comments'] = all_comments

        return JsonResponse(temp_list, status=200)
    else:
        capsule = Capsule.objects.get(cid=cid)

        authorized = check_authorized(cid, request.user.username, 'edit')
        if isinstance(authorized, JsonResponse):
            return authorized

        fields = json.loads(request.body)
        del(fields['owner'])
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
            setattr(capsule, field, fields[field])
        capsule.save()
        return JsonResponse({"status": "resource modified", "cid": capsule.cid}, status=200)


@api_view(['GET'])
def get_media(request, mid):
    media = Media.objects.filter(mid=mid).get()
    authorized = check_authorized(media.cid.cid, request.user.username, 'view')
    if isinstance(authorized, JsonResponse):
        return authorized
    if not media:
        return Response({"status": "No media matches given query."}, status=404)
    filename = media.file.name.split('/')[-1]
    response = HttpResponse(media.file, content_type='image/*')
    response['Content-Disposition'] = 'attatchment; filename=%s' % filename
    return response


@api_view(['GET'])
def get_letters(request, lid):
    letter = Letter.objects.filter(lid=lid).values('title', 'text', 'lid', 'owner', 'capsule_id')
    authorized = check_authorized(letter[0]['capsule_id'], request.user.username, 'view')
    if isinstance(authorized, JsonResponse):
        return authorized
    if not letter:
        return Response({"status": "No Letters match given query."}, status=404)
    returnable = list(letter)[0]
    returnable['cid'] = returnable['capsule_id']
    del returnable['capsule_id']
    return JsonResponse(returnable, status=200)


@api_view(['POST'])
def add_media(request, cid):
    capsule = Capsule.objects.filter(cid=cid).get()
    authorized = check_authorized(cid, request.user.username, 'add')
    if isinstance(authorized, JsonResponse):
        return authorized
    owner = request.user
    media = Media(owner=owner, capsule=capsule)
    media.save()
    media.file = request.FILES['file']
    media.save()
    return JsonResponse({"status": "resource created", "mid": media.mid}, status=200)


@api_view(['POST'])
def add_letters(request, cid):
    authorized = check_authorized(cid, request.user.username, 'add')
    if isinstance(authorized, JsonResponse):
        return authorized
    fields = json.loads(request.body)
    fields['capsule'] = Capsule.objects.filter(cid=cid).get()
    fields['owner'] = request.user
    letter = Letter(**fields)
    letter.save()
    return JsonResponse({"status": "resource created", "lid": letter.lid}, status=200)


@api_view(['POST'])
def add_comments(request, cid):
    authorized = check_authorized(cid, request.user.username, 'add')
    if isinstance(authorized, JsonResponse):
        return authorized
    fields = json.loads(request.body)
    fields['owner'] = request.user
    fields['capsule'] = Capsule.objects.filter(cid=cid).get()
    comment = Comment(**fields)
    comment.save()
    return JsonResponse({"status": "resource created", "comid": comment.comid}, status=200)


# Returns true if authorized, a JsonResponse otherwise
def check_authorized(cid, username, action):
    capsule = Capsule.objects.filter(cid=cid).get()
    if action == 'edit':
        if capsule.owner.username != username:
            return JsonResponse({"status": "Not Authorized"}, status=401)
    elif action == 'add':
        if capsule.owner.username != username and\
                not any(username == user['username'] for user in capsule.contributors.values('username')):
            return JsonResponse({"status": "Not Authorized"}, status=401)
    elif action == 'view':
        if capsule.unlocks_at > utc.localize(datetime.now()) and\
                any(username == user['username'] for user in capsule.recipients.values('username')):
            return JsonResponse({"status": "Capsule is locked. Check back later!"}, status=401)
        if capsule.owner.username != username and\
                not any(username == user['username'] for user in capsule.contributors.values('username')) and\
                not any(username == user['username'] for user in capsule.recipients.values('username')):
            return JsonResponse({"status": "Not Authorized"}, status=401)
        return True
    else:
        return JsonResponse({"status": "Not Authorized", "reason": "Programmer Error"}, status=401)
