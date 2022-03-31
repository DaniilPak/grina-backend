import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core import serializers

# Auth dependencies
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# Redirect dependencies
from django.http import HttpResponseRedirect
from django.urls import reverse

# Hash 256
from hashlib import sha256


# API for courses & videotests(videocards)

def index(request):
    course_objects = serializers.serialize('json', Course.objects.all())
    edit_data = json.loads(course_objects)
    
    for idx, item in enumerate(edit_data):
        data_object = Data.objects.get(id=idx+1)
        json_data_object = serializers.serialize('python', [data_object])
        json_subcourses_object = serializers.serialize('python', data_object.sub_courses.all())
        item['fields']['section'] = 'editted section'
        item['fields']['data'] = json_data_object[0]['fields']
        item['fields']['data']['sub_courses'] = json_subcourses_object

    course_objects = json.dumps(edit_data)
    context = {
        'data': course_objects,
    }
    return render(request, 'grina/index.html', context)

def get_videotest(request, videotest_id):
    videotest = VideoTest.objects.get(id=videotest_id)
    videotest_data = serializers.serialize('python', [videotest])
    # Editing
    json_server_choice_1 = serializers.serialize('python', [videotest.server_choice_1])
    json_server_choice_2 = serializers.serialize('python', [videotest.server_choice_2])
    json_server_choice_3 = serializers.serialize('python', [videotest.server_choice_3])
    json_server_choice_4 = serializers.serialize('python', [videotest.server_choice_4])
    videotest_data[0]['fields']['server_choice_1'] = json_server_choice_1[0]
    videotest_data[0]['fields']['server_choice_2'] = json_server_choice_2[0]
    videotest_data[0]['fields']['server_choice_3'] = json_server_choice_3[0]
    videotest_data[0]['fields']['server_choice_4'] = json_server_choice_4[0]

    context = {
        'videotest_data': json.dumps(videotest_data),
    }
    return render(request, 'grina/get_videotest.html', context)

# Register, Login, Saving Progress

def register_new_user(request):
    email = request.GET['email']
    password = request.GET['password']

    user = User.objects.create_user(email, email, password)
    user.save()

    # Create user data as a storage
    input_ = email + password
    user_token = sha256(input_.encode('utf-8')).hexdigest()
    user_data = UserData(user_token=user_token, user_owner=user)
    user_data.save()

    # Giving user_token to user
    user_token_list = {
        'user_token': user_token
    }

    context = {
        'user_token_list': json.dumps(user_token_list),
    }

    return render(request, 'grina/get_user_token.html', context)

def login_user(request):
    email = request.GET['email']
    password = request.GET['password']

    user = authenticate(request, username=email, password=password)
    if user is not None:
        user_data = UserData.objects.get(user_owner=user)
        user_data_json = serializers.serialize('python', [user_data])
        context = {
            'user_data': json.dumps(user_data_json),
        }
        return render(request, 'grina/get_user_data.html', context)
    else:
        return HttpResponse('Not OK')

# Google Register, Login

def register_new_user_google(request):
    google_email = request.GET['google_email']
    google_token = sha256(google_email.encode('utf-8')).hexdigest()

    user = User.objects.create_user(google_email, google_email, google_token)
    user.save()

    google_user_data = UserData(user_token=google_token, user_owner=user)
    google_user_data.save()

    # Giving user_token to user
    user_token_list = {
        'user_token': google_token
    }

    context = {
        'user_token_list': json.dumps(user_token_list),
    }

    return render(request, 'grina/get_user_token.html', context)

def login_user_google(request):
    google_email = request.GET['google_email']
    google_token = sha256(google_email.encode('utf-8')).hexdigest()

    google_user_data = UserData.objects.get(user_token=google_token)
    google_user_data_json = serializers.serialize('python', [google_user_data])

    context = {
        'user_data': json.dumps(google_user_data_json),
    }

    return render(request, 'grina/get_user_data.html', context)