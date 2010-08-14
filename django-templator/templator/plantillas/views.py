from django.http import Http404
from django.shortcuts import get_object_or_404

from templator.plantillas import loader
from templator.plantillas.models import Collection
from templator.plantillas.utils import (get_context_from_request,
                                        template_to_response)

def template_render(request, collection_name, template_name):
    # TODO: auth?
    collection = get_object_or_404(Collection, name=collection_name)
    if not template_name:
        raise Http404

    # store collection in loader's thread local context
    loader.set_context(collection=collection)

    context = get_context_from_request(request)
    return template_to_response(template_name, context, request=request)
