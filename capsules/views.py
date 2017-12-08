# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from datetime import datetime
from django.http import JsonResponse, HttpResponse, Http404
from pytz import utc

from capsoul import tasks
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import os, capsoul.settings
from database.models import Capsule, User, Media, Letter, Comment

# Email Calling Functions
def capsule_created_emails(sender, instance):
    capsule = Capsule.objects.filter(cid=instance, deleted=False).get()
    send_to = []
    
    for person in capsule.contributors.all():
        send_to.append(person.email)

    for person in capsule.recipients.all():
        send_to.append(person.email)
    
    send_to.append(capsule.owner.email)

    for s in send_to:
        tasks.send_capsule_created_email.apply_async(args=[s], countdown=1)

def capsule_unlocked_emails(sender, instance):
    capsule = Capsule.objects.filter(cid=instance, deleted=False).get()
    send_to = []
    
    for person in capsule.contributors.all():
        send_to.append(person.email)

    for person in capsule.recipients.all():
        send_to.append(person.email)
    
    send_to.append(capsule.owner.email)

    for s in send_to:
        tasks.send_capsule_unlocked_email.apply_async(args=[s], eta=capsule.unlocks_at)


@api_view(['GET', 'POST'])
def all_capsules(request):
    if request.method == 'GET':
        all_capsules = Capsule.objects.all()
        capsules_output = {"capsules": []}
        for capsule in all_capsules:
            current_capsule = {key: getattr(capsule, key) for key in ['cid', 'unlocks_at', 'title']}
            current_capsule['owner'] = capsule.owner.username
            current_capsule['recipients'] = [recipient.username for recipient in capsule.recipients.all()]
            current_capsule['contributors'] = [contributor.username for contributor in capsule.contributors.all()]

            capsules_output['capsules'].append(current_capsule)
        return JsonResponse(capsules_output, status=200)
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
        capsule_created_emails(instance=capsule.cid, sender=Capsule)
        capsule_unlocked_emails(instance=capsule.cid, sender=Capsule)

        return Response({"status": "resource created", "cid": capsule.cid}, status=200)


@api_view(['GET', 'POST', 'DELETE'])
def specific_capsule(request, cid):
    if request.method == "GET":
        capsule = Capsule.objects.filter(cid=cid, deleted=False)
        if not capsule:
            raise Http404("No capsule matches the given query.")
        authorized = check_authorized(Capsule, cid, request.user.username, 'view')
        if isinstance(authorized, JsonResponse):
            return authorized
        try:
            media = Media.objects.filter(capsule=capsule.get(), deleted=False)
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

        contribs = []
        for u in capsule.get().contributors.all():
            contribs.append(u.username)
        temp_list['contributors'] = contribs

        recips = []
        for u in capsule.get().recipients.all():
            recips.append(u.username)
        temp_list['recipients'] = recips

        try:
            letters = Letter.objects.filter(capsule=capsule.get(), deleted=False).values('lid')
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
    elif request.method == "POST":
        capsule = Capsule.objects.get(cid=cid, deleted=False)
        if not capsule:
            raise Http404("No capsule matches the given query.")
        authorized = check_authorized(Capsule, cid, request.user.username, 'edit')
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
        return JsonResponse({"status": "capsule modified", "cid": capsule.cid}, status=200)
    elif request.method == "DELETE":
        capsule = Capsule.objects.get(cid=cid, deleted=False)
        if not capsule:
            raise Http404("No capsule matches the given query.")
        authorized = check_authorized(Capsule, cid, request.user.username, 'delete')
        if isinstance(authorized, JsonResponse):
            return authorized

        capsule.deleted = True
        capsule.save()
        return JsonResponse({"status": "capsule deleted", "cid": capsule.cid}, status=200)


@api_view(['GET', 'DELETE'])
def get_media(request, mid):
    if request.method == 'GET':
        media = Media.objects.filter(mid=mid, deleted=False).get()
        authorized = check_authorized(Capsule, media.capsule.cid, request.user.username, 'view')
        if isinstance(authorized, JsonResponse):
            return authorized
        if not media:
            return Response({"status": "No media matches given query."}, status=404)
        filename = media.file.name.split('/')[-1]
        response = HttpResponse(media.file, content_type='image/*')
        response['Content-Disposition'] = 'attatchment; filename=%s' % filename
        return response
    elif request.method == 'DELETE':
        media = Media.objects.filter(mid=mid, deleted=False).get()
        authorized = check_authorized(Media, mid, request.user.username, 'delete')
        if isinstance(authorized, JsonResponse):
            return authorized
        if not media:
            return Response({"status": "No media matches given query."}, status=404)
        media.deleted = True
        media.save()
        return JsonResponse({"status": "media deleted", "mid": media.mid}, status=200)


@api_view(['GET', 'DELETE'])
def get_letters(request, lid):
    if request.method == 'GET':
        letter = Letter.objects.filter(lid=lid, deleted=False).values('title', 'text', 'lid', 'owner', 'capsule_id')
        authorized = check_authorized(Capsule, letter[0]['capsule_id'], request.user.username, 'view')
        if isinstance(authorized, JsonResponse):
            return authorized
        if not letter:
            return Response({"status": "No Letters match given query."}, status=404)
        returnable = list(letter)[0]
        returnable['cid'] = returnable['capsule_id']
        del returnable['capsule_id']
        return JsonResponse(returnable, status=200)
    elif request.method == 'DELETE':
        letter = Letter.objects.filter(lid=lid, deleted=False).get()
        authorized = check_authorized(Letter, lid, request.user.username, 'delete')
        if isinstance(authorized, JsonResponse):
            return authorized
        if not letter:
            return Response({"status": "No media matches given query."}, status=404)
        letter.deleted = True
        letter.save()
        return JsonResponse({"status": "letter deleted", "lid": letter.lid}, status=200)


@api_view(['POST'])
def add_media(request, cid):
    capsule = Capsule.objects.filter(cid=cid, deleted=False).get()
    authorized = check_authorized(Capsule, cid, request.user.username, 'add')
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
    authorized = check_authorized(Capsule, cid, request.user.username, 'add')
    if isinstance(authorized, JsonResponse):
        return authorized
    fields = json.loads(request.body)
    fields['capsule'] = Capsule.objects.filter(cid=cid, deleted=False).get()
    fields['owner'] = request.user
    letter = Letter(**fields)
    letter.save()
    return JsonResponse({"status": "resource created", "lid": letter.lid}, status=200)


@api_view(['POST'])
def add_comments(request, cid):
    authorized = check_authorized(Capsule, cid, request.user.username, 'add')
    if isinstance(authorized, JsonResponse):
        return authorized
    fields = json.loads(request.body)
    fields['owner'] = request.user
    fields['capsule'] = Capsule.objects.filter(cid=cid, deleted=False).get()
    comment = Comment(**fields)
    comment.save()
    return Response({"status": "resource created", "comid": comment.comid}, status=status.HTTP_201_CREATED)


def check_authorized(model, pk, username, action):
    if model != Capsule:
        obj = model.objects.filter(pk=pk, deleted=False).get()
        if action in ['delete']:
            if obj.owner.username != username:
                return JsonResponse({"status": "Not Authorized"}, status=401)
        pk = obj.capsule.pk
    capsule = Capsule.objects.filter(cid=pk, deleted=False).get()
    if action in ['edit', 'delete']:
        if capsule.owner.username != username:
            return JsonResponse({"status": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    elif action == 'add':
        if capsule.owner.username != username and\
                not any(username == user['username'] for user in capsule.contributors.values('username')):
            return JsonResponse({"status": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    elif action == 'view':
        if capsule.unlocks_at > datetime.now(utc) and\
                any(username == user['username'] for user in capsule.recipients.values('username')):
            return JsonResponse({"status": "Capsule is locked. Check back later!"}, status=status.HTTP_401_UNAUTHORIZED)
        if capsule.owner.username != username and\
                not any(username == user['username'] for user in capsule.contributors.values('username')) and\
                not any(username == user['username'] for user in capsule.recipients.values('username')):
            return JsonResponse({"status": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return True
    else:
        return JsonResponse({"status": "Not Authorized", "reason": "Programmer Error"}, status=status.HTTP_401_UNAUTHORIZED)
