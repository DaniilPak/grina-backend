from distutils.command.upload import upload
from email.mime import image
from operator import mod
from pyexpat import model
from secrets import choice
from xmlrpc.client import Server
from django.db import models
# AUTH MODEL 
from django.contrib.auth.models import User

# Create your models here.

# Sections & Courses & SubCourses

class SubCourse(models.Model):
    id = models.AutoField(primary_key=True)
    subcourse_title = models.CharField(max_length=100)
    api_link_cards = models.URLField()
    api_link_tests = models.URLField()

class Data(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    img_uri = models.URLField()
    sub_courses = models.ManyToManyField(SubCourse)

class Course(models.Model):
    section = models.CharField(max_length=100)
    data = models.ManyToManyField(Data, blank=True)
    
# VideoTests 

class ServerChoice(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField()
    choice_index = models.IntegerField()

class VideoTest(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.FileField(upload_to='grinavideos')
    poster = models.URLField()
    tip = models.CharField(max_length=200)
    server_choice_1 = models.ForeignKey(ServerChoice, on_delete=models.CASCADE, related_name='sc1')
    server_choice_2 = models.ForeignKey(ServerChoice, on_delete=models.CASCADE, related_name='sc2')
    server_choice_3 = models.ForeignKey(ServerChoice, on_delete=models.CASCADE, related_name='sc3')
    server_choice_4 = models.ForeignKey(ServerChoice, on_delete=models.CASCADE, related_name='sc4')

class VideoTestStack(models.Model):
    id = models.AutoField(primary_key=True)
    videotests = models.ManyToManyField(VideoTest, blank=True)

# VideoCards 

class VideoCard(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.FileField(upload_to='grinavideos')
    tip = models.CharField(max_length=200)
    eng_text = models.CharField(max_length=500)
    rus_text = models.CharField(max_length=500)

class VideoCardStack(models.Model):
    id = models.AutoField(primary_key=True)
    videocards = models.ManyToManyField(VideoCard, blank=True)

# Register, Login, Save Progress

class UserData(models.Model):
    user_token = models.CharField(max_length=256)
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE)