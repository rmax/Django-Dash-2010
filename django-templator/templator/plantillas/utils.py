from django.http import HttpResponse, HttpResponseServerError
from django.template.loader import render_to_string

from templator.plantillas.reporter import ExceptionReporter

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
        content = reporter.get_traceback_html(strip_frames=5,
                                              context=context)
        return HttpResponseServerError(content, mimetype='text/html')
    else:
        # TODO: get mimetype from template_name
        return HttpResponse(content, mimetype='text/html')
