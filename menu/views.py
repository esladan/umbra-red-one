from django.shortcuts import render
from django.http import HttpResponse, request, HttpResponseRedirect
from django.views import View
from django.contrib import auth, messages
from django.shortcuts import render, redirect


# Create your views here.


def menu(request):
    print
    return render(request,'menu/menu.html')