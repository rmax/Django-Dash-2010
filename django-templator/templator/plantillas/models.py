from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

class Collection(models.Model):
    name = models.CharField(_(u"Name"), max_length=30, db_index=True)
    owner = models.ForeignKey(User, related_name='mycollections')
    members = models.ManyToManyField(User, related_name='collections',
                                     blank=True, null=True)

    def __unicode__(self):
        return self.name

class Template(models.Model):
    collection = models.ForeignKey(Collection, related_name='templates')
    path = models.CharField(_(u"Path"), max_length=128, db_index=True)
    content = models.TextField()

    def __unicode__(self):
        return self.path
