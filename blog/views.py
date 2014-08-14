from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime
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
            request.session['username'] = username
            return HttpResponse('ok')
    else:
        rf = RegisterForm()
        try:
            del request.session['username']
        except KeyError:
            pass
    return render_to_response('register.html', {'registerform': rf})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        lf = LoginForm(request.POST)
        if lf.is_valid():
            username = lf.cleaned_data['username']
            password = lf.cleaned_data['password']
            user = User.objects.filter(username__exact=username, password__exact=password)
            if user:
                request.session['username'] = username
                return HttpResponseRedirect('/%s/home/' % username)
            user = User.objects.select_related().filter(email__exact=username, password__exact=password)
            if user:
                username = user.username
                request.session['username'] = username
                return HttpResponseRedirect('/%s/home/' % username)
            else:
                error_message = 'Username or Password incorrect'
                lf.cleaned_data['password'] = ''
                return render_to_response('login.html', {'loginform': lf, 'error_message': error_message})
    else:
        username = request.session.get('username', '')
        if not username or not User.objects.filter(username=username):
            lf = LoginForm()
            return render_to_response('login.html', {'loginform': lf})
        else:
            return HttpResponseRedirect('/%s/home/' % username)


def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return HttpResponse('logout')


def home(request, username):
    user = get_object_or_404(User, username=username)
    if request.session.get('username', '') == username:
        user_self = True
    else:
        user_self = False
    blog_list = user.blog_set.select_related().all()
    return render_to_response('home.html', {'blog_list': blog_list, 'username': username, 'user_self': user_self})


def view(request, username, pid):
    user = get_object_or_404(User, username=username)
    blog = get_object_or_404(Blog, author=user, id=pid)
    return render_to_response('view.html', {'blog': blog})


@csrf_exempt
def edit(request, username, pid=''):
    if request.session.get('username', '') == username:
        if request.method == 'POST':
            bf = BlogForm(request.POST)
            if bf.is_valid():
                format_time = '%F %T'
                user = User.objects.get(username=username)
                title = bf.cleaned_data['title']
                content = bf.cleaned_data['content']
                modified_time = datetime.now().strftime(format_time)
                print(modified_time)
                if not pid:
                    blog = Blog.objects.create(author=user, created_time=modified_time)
                else:
                    blog = get_object_or_404(Blog, id=pid)
                blog.title = title
                blog.modified_time = modified_time
                blog.content = content
                blog.save()
                return HttpResponseRedirect('/%s/home/' % username)
        else:
            bf = BlogForm()
            if pid:
                blog = Blog.objects.select_related().filter(id=pid)
                bf.title = blog.title
                bf.content = blog.content
            return render_to_response('edit.html', {'blogform': bf})
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def comment(request):
    pass


@csrf_exempt
def upload(request):
    pass