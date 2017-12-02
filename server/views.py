import uuid

import null as null
from copy import deepcopy
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.utils import json

from server.models import Users, Sound
from server.serializer import UserSerializer, SoundSerializer


@csrf_exempt
def user_list(request):
    """List all users"""
    if request.method == 'GET':
        user = Users.objects.all()
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data,safe= False,status=200)
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET','POST','PUT'])
def create_update_user(request,format=None):

    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse('fail',safe=False,status = status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def sound_detail(request,pk):
    try:
        if pk == null:
            sound = Sound.objects.all()
            return  JsonResponse(serializer.data,safe=False,status=200)
        sound = Sound.objects.get(pk == pk)
    except Sound.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SoundSerializer(sound)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SoundSerializer(sound, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        sound.delete()
        return HttpResponse(status=204)

@csrf_exempt
def sound_list(request):
    if request.method == 'GET':
        snippets = Sound.objects.all()
        serializer = SoundSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SoundSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET','POST','PUT'])
def create_label(request,format=None):
    if request.method == 'POST':
        serializer = SoundSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status = 201)
    return JsonResponse(serializer.error_messages,safe=False,status=400)

@csrf_exempt
@api_view(['GET','POST','PUT'])
def label_random(request,format=None):
    if request.method == 'POST':
        serializer = SoundSerializer(data= {'label':str(uuid.uuid4())})
        if serializer.is_valid():
            serializer.save()
            question = "New label created: "   + str(serializer.data)
            return JsonResponse(serializer.data,safe=False,status = 201)
    return JsonResponse(serializer.error_messages,safe=False,status=400)
