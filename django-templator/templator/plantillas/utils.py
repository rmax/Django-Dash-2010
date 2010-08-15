import mimetypes
import uuid

from django import shortcuts
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseServerError
from django.template.loader import render_to_string
from django.utils import simplejson

from templator.plantillas.reporter import ExceptionReporter


SAFE_MIMES = (
    'text/html',
    'text/plain',
    'text/css'
)

DEFAULT_MIME = 'text/plain'


class JsonResponse(HttpResponse):
    def __init__(self, data):
        content = simplejson.dumps(data, cls=DjangoJSONEncoder)
        super(JsonResponse, self).__init__(content, mimetype="application/json")


def get_object_or_none(klass, *args, **kwargs):
    queryset = shortcuts._get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None

def get_context_from_request(request):
    """
    Fills context from GET and POST. POST take precedence over GET.
    """
    context = {}
    for name in ('GET', 'POST'):
        source = getattr(request, name)
        for name in source.keys():
            # variables ending with [] are retrieved as lists
            if name.endswith('[]'):
                context[name[:-2]] = source.getlist(name)
            else:
                context[name] = source.get(name)

    return context

def template_to_response(template_name, context=None, request=None):
    """
    Renders given template to response. If an exception is caugth
    it renders friendly exception report in html.
    """
    # Loader takes care of which template to load
    # if it fails, use our custom exception reporter without
    # system information, just template-related stuff.
    context = context or {}
    try:
        content = render_to_string(template_name, context)
    except:
        # request is needed just in exception case
        import sys
        reporter = ExceptionReporter(request, *sys.exc_info())
        content = reporter.get_traceback_html(strip_frames=4,
                                              context=context)
        return HttpResponseServerError(content, mimetype='text/html')
    else:
        mimetype, encoding = mimetypes.guess_type(template_name)
        if mimetype not in SAFE_MIMES:
            mimetype = DEFAULT_MIME

        return HttpResponse(content, mimetype=mimetype)

def uuid_hex():
    return uuid.uuid4().hex
