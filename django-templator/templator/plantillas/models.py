from django.db import models
from django.utils.translation import ugettext as _

from templator.plantillas.fields import UUIDField


class TemplateContext(models.Model):
    group_uuid = UUIDField(db_index=True)
    context = models.TextField()


class Template(models.Model):
    group_uuid = UUIDField(db_index=True)
    path = models.CharField(_(u"Path"), max_length=128, db_index=True)
    content = models.TextField()

    def __unicode__(self):
        return self.path
