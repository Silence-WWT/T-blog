from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
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
                return render_to_response('register.html', {'register_form': rf, 'error_message': error_message})
            User.objects.create(username=username, password=password, email=email)
            request.session['username'] = username
            return HttpResponse('ok')
    else:
        rf = RegisterForm()
        try:
            del request.session['username']
        except KeyError:
            pass
    return render_to_response('register.html', {'register_form': rf})


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
                username = user[0].username
                request.session['username'] = username
                return HttpResponseRedirect('/%s/home/' % username)
            else:
                error_message = 'Username or Password incorrect'
                lf.cleaned_data['password'] = ''
                return render_to_response('login.html', {'login_form': lf, 'error_message': error_message})
    else:
        username = request.session.get('username', '')
        if not username or not User.objects.filter(username=username):
            lf = LoginForm()
            return render_to_response('login.html', {'login_form': lf})
        else:
            return HttpResponseRedirect('/%s/home/' % username)


def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return HttpResponse('logout')


def blog(request, username, page=''):
    user = get_object_or_404(User, username=username)
    if request.session.get('username', '') == username:
        user_self = True
    else:
        user_self = False
    blog_list = list(user.blog_set.all().order_by('created_time').reverse())
    try:
        page = int(page)
    except TypeError:
        page = 1
    pages = int((len(blog_list) + 10 - 1) / 10)
    if pages == 0:
        return render_to_response('blog.html', {'blog_list': blog_list, 'username': username, 'user_self': user_self,
                                                'pages': pages})
    if page > pages or page < 1:
        return HttpResponseRedirect('/%s/blog/' % username)
    if pages == 1:
        return render_to_response('blog.html', {'blog_list': blog_list, 'username': username, 'user_self': user_self,
                                                'pages': pages})
    else:
        return render_to_response('blog.html', {'blog_list': blog_list[(page-1)*10: page*10], 'username': username,
                                                'user_self': user_self, 'pages': pages, 'page': page,
                                                'last_page': page-1, 'next_page': page+1, 'range': range(1, pages+1)})


def home(request, username):
    get_object_or_404(User, username=username)
    return render_to_response('home.html', {'username': username})


def view(request, username, pid):
    user = get_object_or_404(User, username=username)
    article = get_object_or_404(Blog, author=user, pk=pid)
    article_list = list(Blog.objects.order_by('created_time').reverse())
    index = article_list.index(article)
    if index > 0:
        next_article = article_list[index - 1]
    else:
        next_article = None
    if index < len(article_list) - 1:
        last_article = article_list[index + 1]
    else:
        last_article = None
    if request.session.get('username', '') == username:
        user_self = True
    else:
        user_self = False
    return render_to_response('view.html', {'username': username, 'blog': article, 'user_self': user_self,
                                            'next': next_article, 'last': last_article})


@csrf_exempt
def edit(request, username, pid=''):
    if request.session.get('username', '') == username:
        if request.method == 'POST':
            bf = BlogForm(request.POST)
            if bf.is_valid():
                if bf.cleaned_data['delete'] is True:
                    if pid:
                        Blog.objects.get(pk=pid).delete()
                    return HttpResponseRedirect('/%s/blog' % username)
                user = User.objects.get(username=username)
                title = bf.cleaned_data['title']
                content = bf.cleaned_data['content']
                if not pid:
                    article = Blog.objects.create(author=user)
                    created_time = datetime.now()
                    created_time = datetime(created_time.year, created_time.month, 1)
                    blog_month = BlogMonth.objects.filter(month__exact=created_time)
                    if not blog_month:
                        month = BlogMonth.objects.create(month=created_time)
                        article.month = month
                    else:
                        article.month = blog_month[0]
                else:
                    article = get_object_or_404(Blog, pk=pid)
                article.title = title
                article.content = content
                article.save()
                return HttpResponseRedirect('/%s/view/%s' % (username, article.pk))
        else:
            if pid:
                article = Blog.objects.filter(pk=pid)
                if not blog:
                    return HttpResponse('no such blog!')
                bf = BlogForm(initial={'title': article[0].title, 'content': article[0].content})
            else:
                bf = BlogForm()
            return render_to_response('edit.html', {'blog_form': bf, 'username': username, 'blog_id': pid})
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def comment(request):
    pass


@csrf_exempt
def upload(request):
    pass