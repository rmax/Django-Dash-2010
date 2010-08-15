from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('templator.plantillas.views',
    url(r'^$', 'template_new', name='new'),
    url(r'^c/(?P<uuid>[a-z0-9]+)/$', 'template_copy', name='copy'),
    url(r'^t/(?P<uuid>[a-z0-9]+)/$', 'template_form', name='form'),
    url(r'^r/(?P<uuid>[a-z0-9]+)/(?P<path>.+)$', 'template_render', name='render'),
    url(r'^v/context/$', 'validate_context', name='validate_context'),
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)
