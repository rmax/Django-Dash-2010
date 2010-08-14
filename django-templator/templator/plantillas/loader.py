import threading

from django.db.models import ObjectDoesNotExist
from django.template import TemplateDoesNotExist
from django.template.loader import (BaseLoader,
                                    get_template_from_string,
                                    make_origin)

thread_context = threading.local()

def set_context(**kwargs):
    thread_context.__dict__.update(kwargs)

class Loader(BaseLoader):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        source, path = self.load_template_source(template_name, template_dirs)

        collection = self.get_current_collection()
        name = '<%s: %s>' % (collection.name, path)

        origin = make_origin(name, self.load_template_source, path, None)
        return get_template_from_string(source, origin, name), None

    def load_template_source(self, template_name, template_dirs=None):
        collection = self.get_current_collection()
        if collection:
            try:
                tpl = collection.templates.get(path=template_name)
                return tpl.content, tpl.path
            except ObjectDoesNotExist:
                pass
        raise TemplateDoesNotExist

    def get_current_collection(self):
        return getattr(thread_context, 'collection', None)


