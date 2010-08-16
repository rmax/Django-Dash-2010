# -*- coding: utf-8 -*-
import ast
import itertools

from django.contrib import messages
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.utils.translation import ugettext as _

from templator.plantillas import loader
from templator.plantillas.forms import TemplateContextForm, TemplateForm
from templator.plantillas.models import TemplateContext, Template
from templator.plantillas.utils import (get_context_from_request,
                                        template_to_response,
                                        get_object_or_none,
                                        uuid_hex,
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

def template_new(request):
    """Redirects to template form with new uuid"""
    uuid = uuid_hex() 
    return redirect('form', uuid=uuid)

def template_form(request, uuid):

    context_obj = get_object_or_none(TemplateContext, group_uuid=uuid)
    if not context_obj:
        context_obj = TemplateContext(group_uuid=uuid)

    request.session.setdefault('templates', set())

    if Template.objects.filter(group_uuid=uuid).count():
        uuid_new = False
    else:
        uuid_new = True

    if uuid_new or uuid in request.session['templates']:
        is_owner = True
    else:
        is_owner = False

    is_owner = uuid in request.session['templates']

    if request.POST:
        context_form = TemplateContextForm(request.POST, prefix='c',
                                           instance=context_obj)

        # num of templates expected
        try:
            num_forms = int(request.POST.get('num_forms'))
        except ValueError:
            # at least expect one form
            num_forms = 1

        template_forms = []
        for i in range(num_forms):
            template_forms.append(TemplateForm(request.POST,
                                               prefix='t%d' % i))

        all_forms = [context_form] + template_forms

        # trigger is_valid on all forms
        if all([f.is_valid() for f in all_forms]):
            # clear old templates
            Template.objects.filter(group_uuid=uuid).delete()

            obj = context_form.save(commit=False)
            obj.group_uuid = uuid
            obj.save()

            for form in template_forms:
                obj = form.save(commit=False)
                # only store templates with content
                if obj.content.strip():
                    obj.group_uuid = uuid
                    obj.save()

            # allow ad-hoc ajax request
            if request.is_ajax():
                return JsonResponse({'status': 'ok'})
            else:
                messages.success(request, _(u"Templates saved"))
                return redirect('form', uuid=uuid)
        else:
            # allow ad-hoc ajax request
            if request.is_ajax():
                # TODO: handle/pass form errors to client
                return JsonResponse({'status': 'error'})
            else:
                messages.error(request, _(u"Please correct errors below"))
    else:
        # defaults
        initial_context = {
            'context': "{'deity': 'pony', 'times': [1, 2, 3, 4]}",
        }
        initial_t0 = {
            'path': 'test.txt',
            'content': "I have {{ deity }} powers!",
        }
        initial_t1 = {
            'path': 'include.txt',
            'content': """
{% extends "base.txt" %}
{% block content %}
    {% for n in times %}
        time: {{ n }}
        {% include "test.txt" %}
    {% endfor %}
{% endblock %}""",
}
        initial_t2 = {
            'path': 'base.txt',
            'content': """
Django Dash Templator

{% block content %}
{% endblock %}

darkrho (c) 2010
    """,
        }
        initial_t3 = {
            'path': 'fail.txt',
            'content': """
Show me exception:

    {% foo %}

«{{ deity }} in action»
    """,
        }

        context_form = TemplateContextForm(prefix='c',
                                           instance=context_obj,
                                           initial=initial_context)

        template_forms = []

        templates = Template.objects.filter(group_uuid=uuid)
        if templates:
            for i, tpl in enumerate(templates):
                form = TemplateForm(prefix='t%d' % i, instance=tpl)
                template_forms.append(form)
        else:
            form = TemplateForm(prefix='t0', initial=initial_t0)
            template_forms.append(form)
            form = TemplateForm(prefix='t1', initial=initial_t1)
            template_forms.append(form)
            form = TemplateForm(prefix='t2', initial=initial_t2)
            template_forms.append(form)
            form = TemplateForm(prefix='t3', initial=initial_t3)
            template_forms.append(form)

        num_forms = len(template_forms)

    return render_to_response('plantillas/form.html', {
        'uuid': uuid,
        'num_forms': num_forms,
        'context_form': context_form,
        'template_forms': template_forms,
    }, context_instance=RequestContext(request))

def template_render(request, uuid, path):
    context = get_context(uuid)
    with loader.set_context(template_uuid=uuid):
        return template_to_response(path, context, request=request)

def template_copy(request, uuid):
    new_uuid = uuid_hex()
    obj = get_object_or_none(TemplateContext, group_uuid=uuid)
    templates = Template.objects.filter(group_uuid=uuid)

    if obj and templates:
        TemplateContext.objects.create(group_uuid=new_uuid,
                                       context=obj.context)
        for t in templates:
            Template.objects.create(group_uuid=new_uuid, path=t.path,
                                    content=t.content)

        messages.success(request, _(u"Template copied successfully"))
        return redirect('form', uuid=new_uuid)
    else:
        messages.error(request, _(u"Template not found"))
        return redirect('/')

def get_context(uuid):
    obj = get_object_or_none(TemplateContext, group_uuid=uuid)
    if obj and obj.context:
        # context should contain a valid string
        return ast.literal_eval(obj.context)
    else:
        return {}
