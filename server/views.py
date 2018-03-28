import uuid

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from fcm_django.models import FCMDevice

from server.models import Users, Sound
from server.serializer import UserSerializer, SoundSerializer
from Predict.predict import predict_sound
import json
from fcm.utils import get_device_model
import datetime

@csrf_exempt
def user_list(request):
    """List all users."""
    if request.method == 'GET':
        user = Users.objects.all()
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'POST', 'PUT'])
def create_update_user(request, format=None):
    """Create update user."""
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        # user
        if serializer.is_valid():
        #     )
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse('fail', safe=False, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def sound_detail(request, pk):
    """Show sound detail."""
    try:
        if pk is None:
            sound = Sound.objects.all()
            serializer = SoundSerializer(sound)
            return JsonResponse(serializer.data, safe=False, status=200)
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
    """Show sound list."""
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
@api_view(['GET', 'POST', 'PUT'])
def create_label(request, format=None):
    """Create label."""
    if request.method == 'POST':
        serializer = SoundSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.error_messages, safe=False, status=400)


@csrf_exempt
@api_view(['GET', 'POST', 'PUT'])
def label_random(request, format=None):
    """Random label."""
    serializer = SoundSerializer()
    if request.method == 'POST' or request.method == 'GET':
        serializer = SoundSerializer(data={'label': str(uuid.uuid4())})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=201)
    return JsonResponse(serializer.error_messages, safe=False, status=400)


@csrf_exempt
@api_view(['PUT', 'POST'])
def label_predict(request, format=None):
    """Label predict api."""
    if request.method == 'PUT' or request.method == 'POST':
        """wave = request.GET['wave']
        print (type(wave))
        sr = request.GET['sr']
        time_start = request.GET['time_start']
        
        """
        content = json.loads(request.body)
        wave = content['wave']
        if(wave == []):
            return JsonResponse("wave must be not empty", safe=False, status =400)
        if(type(wave) is not list):
            return JsonResponse("wave must be list", safe=False, status =400)
        sr = content['sr']
        time_start = content['time_start']
        user_id_id = content['user_id_id']
        predicted_labels = predict_sound(time_start, wave, sr,user_id_id)
        serializer = SoundSerializer(
            data={
                'time_start': time_start,
                'wave': wave,
                'label': predicted_labels,
                'user_id_id' : user_id_id
                })
        if serializer.is_valid():
            serializer.save()
            Device = get_device_model()
            my_phone = Device.objects.get(name="An device")
            my_phone.send_message({'mess':serializer.data["label"]}, collapse_key='something')

            return JsonResponse(predicted_labels, safe=False, status=201)
        Device = get_device_model()
        my_phone = Device.objects.get(name="An device")
        my_phone.send_message({'mess':serializer.data["label"]}, collapse_key='something')
        return JsonResponse(predicted_labels, safe=False, status=200)
    return JsonResponse(predicted_labels, safe=False, status=400)

@csrf_exempt
@api_view(['GET'])
def getLabel(request,format=None):
    "get Label"
    if request.method == 'GET':
        #content = json.loads(request.body)
        time_start = request.GET['time_start']
        user_id = request.GET['user_id']
        now = datetime.datetime.now()
        sounds = Sound.objects.filter(user_id=user_id, time_start__range=[time_start,now])
        result = []
        for i in range(0,len(sounds)):
            result.append({
                "time_start" : sounds[i].time_start,
                "label": sounds[i].label
                })
        data ={
            "count": len(result),
            "result": result
        }
        return JsonResponse(data,safe=False, status=200)
    return JsonResponse("fck u",safe = False,status=400)

@csrf_exempt
@api_view(['GET'])
def getSound(request,format=None):
    "get Sound"
    if request.method == 'GET':
        #content = json.loads(request.body)
        time_start = request.GET['time_start']
        user_id = request.GET['user_id']
        sounds = Sound.objects.filter(user_id=user_id, time_start=time_start)
        result = []
        for i in range(0,len(sounds)):
            result.append({
                "time_start" : sounds[i].time_start,
                "sr" : sounds[i].sr,
                "label": sounds[i].label,
                "wave" : sounds[i].wave
                })
        data ={
            "count": len(result),
            "result": result
        }
        return JsonResponse(data,safe=False, status=200)
    return JsonResponse("fck u",safe = False,status=400)

@csrf_exempt
@api_view(['PUT','POST'])
def FCM(request,format=None):
    "Sending Notification"
    if request.method == 'PUT' or request.method == 'POST':
        message = request.GET['mess']
        Device = get_device_model()

        my_phone = Device.objects.get(name="An device")
        my_phone.send_message({'mess':message}, collapse_key='something')

        return JsonResponse("success", safe =False, status=200)
    return JsonResponse(errors,safe=False,status=400)
