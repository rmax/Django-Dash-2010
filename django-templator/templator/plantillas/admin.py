from django.contrib import admin

from templator.plantillas.models import TemplateContext, Template

admin.site.register(TemplateContext)
admin.site.register(Template)
