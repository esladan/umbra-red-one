from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('signin',views.Signin.as_view(), name='signin'),
    path('signup',views.Signup.as_view(), name='signup'),
    path('reset-password',views.Password_reset.as_view(), name='reset-password'), 
    path('logout',views.logout, name='logout'),
    path('profile/<username>',views.profile, name='profile'),
    path('activate/<uidb64>/<token>',views.activate, name='activate'),
    path('reset/<uidb64>/<token>',views.Reset.as_view(), name='reset'),
    path('activate_req/<mail>',views.Activate_req.as_view(),name='activate_req')

]
