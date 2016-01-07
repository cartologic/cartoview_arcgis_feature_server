__author__ = 'kamal'
from django import forms
from django.db import models
from . import APP_NAME
from django.templatetags.static import static
from django.utils.safestring import mark_safe


class ColorWidget(forms.TextInput):
    class Media:
        js = [static(APP_NAME) + "/manager/js/color-picker.js"]

    def render(self, name, value, attrs=None):
        html = super(ColorWidget, self).render(name, value, attrs)
        html += """<script type="text/javascript" charset="utf-8">
(function($){
    $(function(){
        $("#%s").colorPicker();
    })
})(django.jQuery)</script>
        """ % attrs["id"]
        return mark_safe(html)


class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = self.__class__.__module__ + "." + self.__class__.__name__
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
