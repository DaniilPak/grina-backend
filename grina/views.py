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
    # New future json object
    my_arr = list()
    # Fixing Course objects
    for idx, item in enumerate(edit_data):
        # New stuff
        current_course = Course.objects.get(id=idx+1)
        course_datas = serializers.serialize('python', current_course.data.all())
        item['fields']['section'] = 'editted section'
        item['fields']['data'] = course_datas
        # Fixing Data objects
        for idx2, data_item in enumerate(course_datas):
            # Hooking current Data object from Data object primary key  
            current_data = Data.objects.get(pk=json.loads(json.dumps(data_item))['pk'])
            # Removing superfluos from data object in json
            x = serializers.serialize('python', [current_data])
            item['fields']['data'][idx2] = x[0]['fields']
            # Adding id field to data json object
            item['fields']['data'][idx2]['id'] = x[0]['pk']
            # Hooking current SubCourses object from current Data object
            current_datas_subcourses =  serializers.serialize('python', current_data.sub_courses.all())
            item['fields']['data'][idx2]['sub_courses'] = current_datas_subcourses
            # Fixing SubCourse objects
            for idx3, subcourse_item in enumerate(current_datas_subcourses):
                current_subcourse = SubCourse.objects.get(pk=json.loads(json.dumps(subcourse_item))['pk'])
                y = serializers.serialize('python', [current_subcourse])
                item['fields']['data'][idx2]['sub_courses'][idx3] = y[0]['fields']

        # Saving all processed data to future json object
        my_arr.append(item['fields'])

        # Old stuff
        # data_object = Data.objects.get(id=idx+1)
        # json_data_object = serializers.serialize('python', [data_object])
        # json_subcourses_object = serializers.serialize('python', data_object.sub_courses.all())
        
        # item['fields']['data']['sub_courses'] = json_subcourses_object
 
    context = {
        'data': json.dumps(my_arr),
    }
    return render(request, 'grina/index.html', context)

def get_videotest_stack(request, videotest_stack_id):
    videotest_stack = VideoTestStack.objects.get(id=videotest_stack_id)
    videotest_stack_videotests = serializers.serialize('python', videotest_stack.videotests.all())

    my_arr = list()

    for idx, item in enumerate(videotest_stack_videotests):
        # Editing server choice objects
        videotest = VideoTest.objects.get(id=item['pk'])
        json_server_choice_1 = serializers.serialize('python', [videotest.server_choice_1])
        json_server_choice_2 = serializers.serialize('python', [videotest.server_choice_2])
        json_server_choice_3 = serializers.serialize('python', [videotest.server_choice_3])
        json_server_choice_4 = serializers.serialize('python', [videotest.server_choice_4])
        item['fields']['server_choice_1'] = json_server_choice_1[0]['fields']
        item['fields']['server_choice_2'] = json_server_choice_2[0]['fields']
        item['fields']['server_choice_3'] = json_server_choice_3[0]['fields']
        item['fields']['server_choice_4'] = json_server_choice_4[0]['fields']
        # Editing end...
        my_arr.append(item['fields'])

    '''
    videotest = VideoTest.objects.get(id=videotest_stack_id)
    videotest_data = serializers.serialize('python', [videotest])
    # Editing
    json_server_choice_1 = serializers.serialize('python', [videotest.server_choice_1])
    json_server_choice_2 = serializers.serialize('python', [videotest.server_choice_2])
    json_server_choice_3 = serializers.serialize('python', [videotest.server_choice_3])
    json_server_choice_4 = serializers.serialize('python', [videotest.server_choice_4])
    videotest_data[0]['fields']['server_choice_1'] = json_server_choice_1[0]['fields']
    videotest_data[0]['fields']['server_choice_2'] = json_server_choice_2[0]['fields']
    videotest_data[0]['fields']['server_choice_3'] = json_server_choice_3[0]['fields']
    videotest_data[0]['fields']['server_choice_4'] = json_server_choice_4[0]['fields']
    '''
    context = {
        'videotest_data': json.dumps(my_arr),
    }
    return render(request, 'grina/get_videotest_stack.html', context)

def get_videocard_stack(request, videocard_stack_id):
    videocard_stack = VideoCardStack.objects.get(id=videocard_stack_id)
    videocard_stack_videocards = serializers.serialize('python', videocard_stack.videocards.all())

    my_arr = list()
    for idx, item in enumerate(videocard_stack_videocards):
        my_arr.append(item['fields'])

    context = {
        'videocard_data': json.dumps(my_arr),
    }
    return render(request, 'grina/get_videocard_stack.html', context)

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