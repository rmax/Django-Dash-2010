import ast

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from templator.plantillas import loader
from templator.plantillas.models import TemplateContext
from templator.plantillas.utils import (get_context_from_request,
                                        template_to_response,
                                        get_object_or_none,
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

def template_render(request, uuid, path):
    context = get_context(uuid)
    with loader.set_context(template_uuid=uuid):
        return template_to_response(path, context, request=request)

def get_context(uuid):
    obj = get_object_or_none(TemplateContext, group_uuid=uuid)
    if obj and obj.context:
        # context should contain a valid string
        return ast.literal_eval(obj.context)
    else:
        return {}
