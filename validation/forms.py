from django import forms

class ApiSpecificationUrlValidationForm(forms.Form):
    api_specification_url = forms.URLField()

class QuickInlineMetadataValidationForm(forms.Form):
    xml_file_string = forms.CharField()
    xml_file_name = forms.CharField()

class QuickInlineMetadataUpdateValidationForm(QuickInlineMetadataValidationForm):
    existing_metadata_id = forms.CharField()

class InlineXSDMetadataValidationForm(forms.Form):
    xml_file_string = forms.CharField()

class LocalIDValidationForm(forms.Form):
    localid = forms.CharField()