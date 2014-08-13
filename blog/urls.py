from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
                       url(r'^register/$', views.register),
                       url(r'^login/$', views.login),
                       # url(r'^logout/$', views.logout),

                       url(r'^(\w+?)/home/$', views.home),
                       url(r'^(\w+?)/view/(\d+)/$', views.view),
                       url(r'^(\w+?)/add/$', views.add),
                       url(r'^(\w+?)/edit/(\d+)/$', views.edit),
                       )
