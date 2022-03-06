from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import MyUsers, Contact
from django.http import HttpResponse
from .decorators import get_location
import geocoder
import geoip2.database
import requests
import json


# Create your views here.
# @get_location
def home(request):
    return render(request, 'index.html', {'title': 'What We Are'})


def learnmore(request, cat):
    return render(request, 'learnmore.html', {'title': f'{cat.capitalize()} with Python'})


def register(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            print('logged in')
            return redirect('/')
    return render(request, 'login.html')


def SignOut(request):
    logout(request)
    return redirect('/login')


def SignUp(request):
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if username and password and email:
            user = User(email=email, username=username, first_name=first_name, last_name=last_name)
            user.set_password(password)
            my_user = MyUsers(username=user, password=password, first_name=first_name,
                              last_name=last_name, email=email)

            user.save()
            my_user.save()
            print('saved')
            user_auth = authenticate(request, username=username, password=password)
            if user_auth:
                print('log in')
                login(request, user)
                return redirect('/')

    return render(request, 'register.html')


def contact(request):
    print('entered')
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        terms = request.POST.get('terms')

        print(terms)

        if terms and email and len(message) > 10:
            form = ''
            user = list(MyUsers.objects.filter(email=email).values())
            print(user)

            if user:

                user = User.objects.get(email=email)
                form = Contact(full_name=name, email=email, message=message, terms=terms, user=user)
                form.save()

                return HttpResponse('Success')

            else:

                form = Contact(full_name=name, email=email, message=message, terms=terms)
                form.save()

                return HttpResponse('Success')

    return HttpResponse('Invalid Request')


