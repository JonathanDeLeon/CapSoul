# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from datetime import datetime
from django.http import JsonResponse, HttpResponse
from pytz import utc

from rest_framework.decorators import api_view
from rest_framework.response import Response

from database.models import Capsule, User, Media, Letters, Comments


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
            return Response({"status": "No capsule matches the given query."}, status=404)
        if capsule.get().unlocks_at > utc.localize(datetime.now()) and\
                capsule.get().owner.username != request.user.username and\
                request.user.username not in capsule.get().contributors.values('username'):
            return JsonResponse({"status": "Capsule is locked. Check back later!"}, status=401)
        if request.user.username not in capsule.get().recipients.values('username'):
            return JsonResponse({"status": "Not Authorized"}, status=401)
        try:
            media = Media.objects.filter(cid=capsule.get())
        except:
            media = []
        all_media = []
        for m in media:
            all_media.append(m.mid)
        temp_list = list(capsule.values())[0]
        temp_list['media'] = all_media

        try:
            letters = Letters.objects.filter(cid=capsule.get()).get()
        except:
            letters = []
        all_letters = []
        for l in letters:
            all_letters.append(l.lid)
        temp_list['letters'] = all_letters

        return JsonResponse(temp_list, status=200)
    else:
        capsule = Capsule.objects.get(cid=cid)
        if capsule.owner.username != request.user.username:
            return JsonResponse({"status": "Not Authorized"}, status=401)
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
    if not media:
        return Response({"status": "No media matches given query."}, status=404)
    filename = media.file.name.split('/')[-1]
    response = HttpResponse(media.file, content_type='image/*')
    response['Content-Disposition'] = 'attatchment; filename=%s' % filename
    return response

@api_view(['GET'])
def get_letters(request, lid):
    letter = Letters.objects.filter(lid=lid).values('title', 'text', 'lid', 'owner')
    if not letter:
        return Response({"status": "No Letters match given query."}, status=404)
    return JsonResponse(list(letter)[0], status=200)

@api_view(['POST'])
def add_media(request, cid):
    capsule = Capsule.objects.filter(cid=cid).get()
    owner = request.user
    media = Media(owner=owner, cid=capsule)
    media.save()
    media.file = request.FILES['file']
    media.save()
    return JsonResponse({"status": "resource created", "mid": media.mid}, status=200)


@api_view(['POST'])
def add_letters(request, cid):
    capsule = Capsule.objects.filter(cid=cid).get()
    owner = request.user
    letter = Letters(owner=owner, cid=capsule)
    letter.save()
    letter.title = request.POST['title']
    letter.text = request.POST['text']
    letter.save()
    return JsonResponse({"status": "resource created", "lid": letter.lid}, status=200)


@api_view(['POST'])
def add_comments(request, cid):
    capsule = Capsule.objects.filter(cid=cid).get()
    owner = request.user
    comment = Comments(owner=owner, cid=capsule)
    comment.save()
    comment.title = request.POST['title']
    comment.text = request.POST['text']
    comment.save()
    return JsonResponse({"status": "resource created", "comid": comment.comid}, status=200)
