import contextlib
import threading

from django.template import TemplateDoesNotExist
from django.template.loader import (BaseLoader,
                                    get_template_from_string,
                                    find_template_loader,
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

    def __init__(self, loaders):
        self._loaders = loaders
        self._cached_loaders = []

    @property
    def loaders(self):
        if not self._cached_loaders:
            for loader in self._loaders:
                self._cached_loaders.append(find_template_loader(loader))
        return self._cached_loaders

    def load_template(self, template_name, template_dirs=None):
        uuid = self.get_template_uuid()
        if uuid:
            # load from db only
            try:
                tpl = TemplateModel.objects.get(group_uuid=uuid, path=template_name)
            except TemplateModel.DoesNotExist:
                raise TemplateDoesNotExist(template_name)
            else:
                origin = make_origin(tpl.path, self, template_name,
                                     template_dirs)
                return tpl.content, origin
        else:
            # use normal loaders
            return self.find_template(template_name, template_dirs)

    def find_template(self, template_name, template_dirs=None):
        for loader in self.loaders:
            try:
                template, display_name = loader(template_name, template_dirs)
                origin = make_origin(display_name, loader,
                                     template_name, template_dirs)
                return template, origin
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist(template_name)

    def get_template_uuid(self):
        return getattr(thread_context, 'template_uuid', None)

