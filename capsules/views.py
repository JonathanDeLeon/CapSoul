# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from database.models import Capsule, User, Media, Letters, Comments


@require_http_methods(["GET", "POST"])
# @login_required(login_url='/auth-error/')
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
# @login_required(login_url='/auth-error/')
def specific_capsule(request, cid):
    if request.method == "GET":
        capsule = Capsule.objects.filter(cid=cid).values()
        if not capsule:
            raise Http404("No capsule matches the given query.")
        return JsonResponse(list(capsule)[0], status=200)
    else:
        return JsonResponse({"status": "resource created"}, status=200)


@require_GET
# @login_required(login_url='/auth-error/')
def get_media(request, mid):
    media = Media.objects.filter(mid=mid).get()
    if not media:
        raise Http404("No media matches given query.")
    filename = media.file.name.split('/')[-1]
    response = HttpResponse(media.file,content_type='image/*')
    response['Content-Dsiposition'] = 'attatchment; filename=%s' % filename
    return response

@require_GET
# @login_required(login_url='/auth-error/')
def get_letters(request, lid):
    letter = Letters.objects.filter(lid=lid).values('title','text','lid','owner')
    if not letter:
        raise Http404("No Letters match given query.")
    return JsonResponse(list(letter)[0], status=200)

@require_POST
# @login_required(login_url='/auth-error/')
def add_media(request, cid):
    capsule = Capsule.objects.filter(cid=cid).get()
    #owner = User.objects.filter(username='test').get()
    owner = request.user
    media = Media(owner=owner, cid=capsule)
    media.save()
    media.file = request.FILES['file']
    media.save()
    return JsonResponse({"status": "resource created", "mid": media.mid}, status=200)

@require_POST
# @login_required(login_url='/auth-error/')
def add_letters(request, cid):
    capsule = Capsule.objects.filter(cid=cid).get()
    #owner = User.objects.filter(username='test').get()
    owner = request.user
    letter = Letters(owner=owner, cid=capsule)
    letter.save()
    letter.title = request.POST['title']
    letter.text = request.POST['text']
    letter.save()
    return JsonResponse({"status": "resource created", "lid": letter.lid}, status=200)


@require_POST
# @login_required(login_url='/auth-error/')
def add_comments(request, cid):
    capsule = Capsule.objects.filter(cid=cid).get()
    #owner = User.objects.filter(username='test').get()
    owner = request.user
    comment = Comments(owner=owner, cid=capsule)
    comment.save()
    comment.title = request.POST['title']
    comment.text = request.POST['text']
    comment.save()
    return JsonResponse({"status": "resource created", "comid": comment.comid}, status=200)
