import contextlib
import threading

from django.db.models import ObjectDoesNotExist
from django.template import TemplateDoesNotExist
from django.template.loader import (BaseLoader,
                                    get_template_from_string,
                                    make_origin)

from templator.plantillas.models import Template as TemplateModel

thread_context = threading.local()

@contextlib.contextmanager
def set_context(**kwargs):
    try:
        thread_context.__dict__.update(kwargs)
        yield
    finally:
        for k in kwargs:
            thread_context.__dict__.pop(k, None)


class Loader(BaseLoader):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        source, path = self.load_template_source(template_name, template_dirs)

        origin = make_origin(path, self.load_template_source, path, None)
        return get_template_from_string(source, origin, path), None

    def load_template_source(self, template_name, template_dirs=None):
        # fetch template by uuid or content
        template_uuid = self.get_template_uuid()
        template_content = self.get_template_content()

        if template_uuid:
            try:
                tpl = TemplateModel.objects.get(group_uuid=template_uuid,
                                                path=template_name)
                return tpl.content, tpl.path
            except ObjectDoesNotExist:
                pass
        elif template_content:
            return template_content, None

        raise TemplateDoesNotExist

    def get_template_uuid(self):
        return getattr(thread_context, 'template_uuid', None)

    def get_template_content(self):
        return getattr(thread_context, 'template_content', None)

