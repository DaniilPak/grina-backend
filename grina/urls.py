from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('videotest/<int:videotest_id>', views.get_videotest, name='videotest'),
    path('register-new-user/', views.register_new_user, name='register-new-user'),
    path('login_user/', views.login_user, name='login-user'),
    # Google auth
    path('register-new-user-google/', views.register_new_user_google, name='register_new_user_google'),
    path('login-user-google/', views.login_user_google, name='login-user-google'),
    

]