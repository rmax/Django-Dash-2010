import ast

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from templator.plantillas import loader
from templator.plantillas.models import Collection
from templator.plantillas.utils import (get_context_from_request,
                                        template_to_response,
                                        JsonResponse)

def validate_context(request):
    context = request.POST.get('context')
    data = {'status': 'error'}
    if context:
        try:
            ast.literal_eval(context)
            data['status'] = 'ok'
        except SyntaxError as e:
            label = 'Syntax error: '
            msg = '<pre>%s%s<br/>%s</pre>'
            data['message'] = msg % (label, e.text,
                                     "&nbsp;"*(e.offset-1+len(label))+"^")
        except ValueError:
            data['message'] = ("Invalid string. Only strings, numbers, lists "
                               "and dicts supported")
    else:
        data['message'] = "context can't be empty"

    return JsonResponse(data)

def anon_template_render(request):
    context = get_context_from_request(request)

    template_name = context.pop('__name__', '__name__')
    template_content = context.pop('__content__', '')

    if template_content:
        with loader.set_context(template_content=template_content):
            return template_to_response(template_name, context, request=request)
    else:
        return redirect('/')

def template_render(request, collection_name, template_name):
    # TODO: auth?
    collection = get_object_or_404(Collection, name=collection_name)
    if not template_name:
        raise Http404

    # store collection in loader's thread local context
    context = get_context_from_request(request)
    with loader.set_context(collection=collection):
        return template_to_response(template_name, context, request=request)
