import contextlib
import threading

from django.db.models import ObjectDoesNotExist
from django.template import TemplateDoesNotExist
from django.template.loader import (BaseLoader,
                                    get_template_from_string,
                                    make_origin)

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

        collection = self.get_current_collection()
        if collection:
            name = '<%s: %s>' % (collection.name, path)
        else:
            name = None

        origin = make_origin(name, self.load_template_source, path, None)
        return get_template_from_string(source, origin, name), None

    def load_template_source(self, template_name, template_dirs=None):
        collection = self.get_current_collection()
        template_content = self.get_template_content()

        if collection:
            try:
                tpl = collection.templates.get(path=template_name)
                return tpl.content, tpl.path
            except ObjectDoesNotExist:
                pass
        elif template_content:
            return template_content, None

        raise TemplateDoesNotExist

    def get_current_collection(self):
        return getattr(thread_context, 'collection', None)

    def get_template_content(self):
        return getattr(thread_context, 'template_content', None)

