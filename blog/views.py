from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from blog.models import *
from blog.forms import *
import re


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
    blog_list = list(user.blog_set.all().order_by('created_time').reverse())
    return pageinate(request, username, blog_list, page)


def archive(request, username, time, page=''):
    user = get_object_or_404(User, username=username)
    archive_time = datetime(int(time[:4]), int(time[5:]), 1)
    archive_month = get_object_or_404(BlogMonth, month=archive_time, user=user)
    blog_list = list(archive_month.blog_set.all().order_by('created_time').reverse())
    if not blog_list:
        return Http404
    archive_month = archive_month.month.strftime('%Y-%m')
    return pageinate(request, username, blog_list, page, archive_month)


def get_archive_dict_list(user):
    archive_list = list(user.blogmonth_set.all().order_by('month').reverse())
    archive_dict_list = []
    for month in archive_list:
        archive_dict_list.append({'month': month.month.strftime('%Y-%m'), 'num': month.blog_set.count()})
    return archive_dict_list


def category(request, username, tag, page=''):
    user = get_object_or_404(User, username=username)
    category_tag = get_object_or_404(Tag, tag_name=tag, user=user)
    blog_list = list(category_tag.blog_set.all())
    if not blog_list:
        return Http404
    return pageinate(request, username, blog_list, page, category_tag=category_tag.tag_name)


def get_category_dict_list(user):
    category_list = list(user.tag_set.all())
    category_dict_list = []
    for tag in category_list:
        if tag.blog_set.count():
            category_dict_list.append({'category_name': tag.tag_name, 'num': tag.blog_set.count()})
    return category_dict_list


def pageinate(request, username, blog_list, page, archive_month=None, category_tag=None):
    user = User.objects.get(username=username)
    if request.session.get('username', '') == username:
        user_self = True
    else:
        user_self = False
    try:
        page = int(page)
    except TypeError:
        page = 1
    pages = int((len(blog_list) + 10 - 1) / 10)
    if page > pages or page < 1:
        return HttpResponseRedirect('/%s/blog/' % username)
    try:
        uncategorized_tag = get_object_or_404(Tag, tag_name='Uncategorized', user=user)
    except ObjectDoesNotExist:
        uncategorized_tag = None
    context = {'blog_list': blog_list, 'username': username, 'user_self': user_self, 'pages': pages,
               'archive_dict_list': get_archive_dict_list(user), 'archive_month': archive_month,
               'category_dict_list': get_category_dict_list(user), 'category_tag': category_tag,
               'uncategorized_tag': uncategorized_tag}
    if pages > 1:
        context['blog_list'] = blog_list[(page-1)*10: page*10]
        context['page'] = page
        context['last_page'] = page - 1
        context['next_page'] = page + 1
        context['range'] = range(1, pages + 1)
    return render_to_response('blog.html', context)


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
    try:
        uncategorized_tag = get_object_or_404(Tag, tag_name='Uncategorized', user=user)
    except ObjectDoesNotExist:
        uncategorized_tag = None
    context = {'username': username, 'blog': article, 'user_self': user_self, 'next': next_article,
               'last': last_article, 'archive_dict_list': get_archive_dict_list(user),
               'category_dict_list': get_category_dict_list(user), 'uncategorized_tag': uncategorized_tag}
    return render_to_response('view.html', context)


@csrf_exempt
def edit(request, username, pid=''):
    if request.session.get('username', '') == username:
        user = User.objects.get(username=username)
        if request.method == 'POST':
            bf = BlogForm(request.POST)
            if bf.is_valid():
                if bf.cleaned_data['delete'] is True:
                    if pid:
                        Blog.objects.get(pk=pid).delete()
                    return HttpResponseRedirect('/%s/blog' % username)
                title = bf.cleaned_data['title']
                content = bf.cleaned_data['content']
                if not pid:
                    article = Blog.objects.create(author=user)
                    created_time = datetime.now()
                    created_time = datetime(created_time.year, created_time.month, 1)
                    blog_month = BlogMonth.objects.filter(month__exact=created_time, user__exact=user)
                    if not blog_month:
                        month = BlogMonth.objects.create(month=created_time, user=user)
                        article.month = month
                    else:
                        article.month = blog_month[0]
                else:
                    article = get_object_or_404(Blog, pk__exact=pid, author__exact=user)
                tag = re.sub(' ', '', bf.cleaned_data['tag']).split(',')
                tag_list = []
                for item in tag:
                    if item:
                        tag_list.append(item)
                article_tag_list = list(article.tag.all())
                prove_list = []
                if tag_list:
                    for item in tag_list:
                        try:
                            tag = Tag.objects.get(tag_name=item, user=user)
                            if tag not in article.tag.all():
                                article.tag.add(tag)
                            else:
                                prove_list.append(tag)
                        except ObjectDoesNotExist:
                            tag = Tag.objects.create(tag_name=item, user=user)
                            article.tag.add(tag)
                for tag in article_tag_list:
                    if tag not in prove_list:
                        article.tag.remove(tag)
                if not article.tag.count():
                    try:
                        tag = Tag.objects.get(tag_name='Uncategorized', user=user)
                    except ObjectDoesNotExist:
                        tag = Tag.objects.create(tag_name='Uncategorized', user=user)
                    article.tag.add(tag)
                article.title = title
                article.content = content
                article.save()
                return HttpResponseRedirect('/%s/view/%s' % (username, article.pk))
            else:
                return HttpResponse(bf.cleaned_data)
        else:
            if pid:
                try:
                    article = Blog.objects.get(pk=pid, author=user)
                except ObjectDoesNotExist:
                    return Http404
                init_dict = {'title': article.title, 'content': article.content}
                content = article.content
                tag = article.tag.all()
                if tag:
                    tag_list = []
                    for item in tag:
                        tag_list.append(item.tag_name + ', ')
                    tag_str = ''.join(tag_list)
                    init_dict['tag'] = tag_str
                bf = BlogForm(initial=init_dict)
            else:
                bf = BlogForm()
                content = ''
            return render_to_response('edit.html', {'blog_form': bf, 'username': username, 'blog_id': pid,
                                                    'content': content})
    else:
        return HttpResponseRedirect('/login/')


@csrf_exempt
def comment(request):
    pass


@csrf_exempt
def upload(request):
    pass