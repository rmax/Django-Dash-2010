import uuid

from django.db import models

class UUIDField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 32)
        kwargs['blank'] = True

        super(UUIDField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname, None):
            value = self.generate_uuid()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(UUIDField, self).pre_save(model_instance, add)

    def generate_uuid(self):
        return uuid.uuid4().hex
