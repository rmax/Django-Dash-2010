from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('templator.plantillas.views',
    url(r'render/(?P<collection_name>\S+)/(?P<template_name>.*)', 'template_render', name='render'),
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)
