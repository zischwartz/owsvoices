from django.conf.urls.defaults import patterns, include, url
from posts.views import *

from django.views.generic import ListView, DetailView
from django.views.generic.simple import direct_to_template

from posts.models import Post

post_detail = DetailView.as_view(model=Post)
post_list = ListView.as_view(model=Post)


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', Home),
    # url(r'^post/(?P<pk>[a-z\d]+)/$', post_detail, name='post_detail'),
    url(r'^post/(?P<slug>[^/]+)/?$', post_detail, name='post_detail'),
    url(r'^$', post_list, name='post_list'),
    url(r'^post/(?P<slug>[^/]+)/comment/?$', Comment),
    url(r'^about/?$', direct_to_template, {'template': 'about.html'}),
    url(r'^contact/?$', direct_to_template, {'template': 'contact.html'}),
    # url(r'^voices/', include('voices.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )