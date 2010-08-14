from django.http import Http404, HttpResponse, HttpResponseServerError
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from templator.plantillas.models import Collection
from templator.plantillas import loader
from templator.plantillas.reporter import ExceptionReporter

def template_render(request, collection_name, template_name):
    # TODO: auth?
    collection = get_object_or_404(Collection, name=collection_name)
    if not template_name:
        raise Http404

    # store collection in loader's thread local context
    loader.set_context(collection=collection)

    # fill context from GET and POST
    # POST overrides GET variables
    context = {}
    for name in ('GET', 'POST'):
        source = getattr(request, name)
        for name in source.keys():
            # variables ending with [] are retrieved as lists
            if name.endswith('[]'):
                context[name[-2:]] = source.getlist(name)
            else:
                context[name] = source.get(name)

    # Render template. Loader takes care of which template to load
    # if it fails, use our custom exception reporter without
    # system information, just template-related stuff.
    try:
        content = render_to_string(template_name, context)
    except:
        import sys
        reporter = ExceptionReporter(request, *sys.exc_info())
        content = reporter.get_traceback_html(strip_frames=4,
                                              context=context)
        return HttpResponseServerError(content, mimetype='text/html')
    else:
        # TODO: get mimetype from template_name
        return HttpResponse(content, mimetype='text/html')
