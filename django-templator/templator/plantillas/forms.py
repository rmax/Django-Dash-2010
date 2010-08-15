import ast
import re

from django import forms
from django.utils.translation import ugettext as _

from templator.plantillas.models import TemplateContext, Template


class TemplateContextForm(forms.ModelForm):

    class Meta:
        model = TemplateContext
        fields = ('context', )

    def clean_context(self):
        context = self.cleaned_data['context']

        if context.strip():
            try:
                data = ast.literal_eval(context)
                if isinstance(data, dict):
                    return context
                else:
                    message = _(u"context must be a dictionary")
                    raise forms.ValidationError(message)
            except SyntaxError as e:
                message = _(u"you have a syntax error at line %d column %d")
                raise forms.ValidationError(message % (e.lineno, e.offset))
            except ValueError as e:
                message = _(u"value error: %s") % e.msg
                raise forms.ValidationError(message)
            except Exception as e:
                message = _(u"unknown error: %s") % e.msg
                raise forms.ValidationError(message)
        else:
            raise forms.ValidationError(_(u"context required"))


class TemplateForm(forms.ModelForm):

    class Meta:
        model = Template
        fields = ('path', 'content')

    def clean_path(self):
        path = self.cleaned_data['path'].strip()

        if not re.search(r'^[A-Za-z/\\._-]+$', path):
            message = _(u"path contains a invalid character")
            raise forms.ValidationError(message)

        if not re.search(r'^[A-Za-z_]', path):
            message = _(u"path must start with a letter or number")
            raise forms.ValidationError(message)

        return path
