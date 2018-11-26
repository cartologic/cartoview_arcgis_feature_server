__author__ = 'kamal'
from django import forms
from cartoserver.models import FeatureLayer


class FeatureLayerEditForm(forms.ModelForm):
    class Meta:
        model = FeatureLayer
        fields = ('copyright_text', 'has_attachments', 'display_field_name', 'max_records','included_fields_names', 'drawing_info', 'popup', 'initial_query')
