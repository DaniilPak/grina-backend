from ast import Sub
from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Course)
admin.site.register(Data)
admin.site.register(SubCourse)
admin.site.register(ServerChoice)
admin.site.register(VideoTest)
admin.site.register(UserData)
admin.site.register(VideoTestStack)
admin.site.register(VideoCard)
admin.site.register(VideoCardStack)