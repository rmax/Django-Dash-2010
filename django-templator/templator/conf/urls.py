from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('templator.plantillas.views',
    url(r'^r/$', 'anon_template_render', name='anon_render'),
    url(r'^r/(?P<collection_name>\S+)/(?P<template_name>.*)$',
        'template_render', name='render'),
    url(r'^v/context/$', 'validate_context', name='validate_context'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {
        'template': 'index.html',
    }, name='index'),
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)
