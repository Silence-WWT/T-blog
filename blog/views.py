from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from blog.models import *
from blog.forms import *


@csrf_exempt
def register(request):
    if request.method == 'POST':
        rf = RegisterForm(request.POST)
        if rf.is_valid():
            username = rf.cleaned_data['username']
            password = rf.cleaned_data['password']
            confirm_password = rf.cleaned_data['confirm_password']
            email = rf.cleaned_data['email']
            error = False
            error_message = []
            if User.objects.filter(username=username):
                error = True
                error_message.append('Username exists. ')
            if password != confirm_password:
                error = True
                error_message.append('Passwords not equal. ')
            if User.objects.filter(email=email):
                error = True
                error_message.append('Email exists.')
            if error:
                rf.cleaned_data['password'] = ''
                rf.cleaned_data['confirm_password'] = ''
                error_message = ''.join(error_message)
                return render_to_response('register.html', {'registerform': rf, 'error_message': error_message})
            register_date = date.today()
            User.objects.create(username=username, password=password, email=email, register_date=register_date)
            return HttpResponse('ok')
    else:
        rf = RegisterForm()
    return render_to_response('register.html', {'registerform': rf})


@csrf_exempt
def login(request):
    pass


def logout(request):
    pass


def home(request, username):
    pass


def view(request, username, pid):
    pass


@csrf_exempt
def add(request, username):
    pass

@csrf_exempt
def edit(request, pid):
    pass


@csrf_exempt
def comment(request):
    pass

@csrf_exempt
def upload(request):
    pass