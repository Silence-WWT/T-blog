from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.login, name='login'),
                       url(r'^logout/$', views.logout, name='logout'),

                       url(r'^(\w+?)/home/$', views.home, name='home'),
                       url(r'^(\w+?)/blog/(?:(\d+)/)?$', views.blog, name='blog'),
                       url(r'^(\w+?)/view/(\d+)/$', views.view, name='view'),
                       url(r'^(\w+?)/edit/(?:(\d+)/)?$', views.edit, name='edit'),
                       url(r'^(\w+?)/archive/(\d{4}-\d{2})/(?:(\d+)/)?$', views.archive, name='archive'),
                       url(r'^(\w+?)/category/(\w+?)/(?:(\d+)/)?$', views.category, name='category'),
                       )