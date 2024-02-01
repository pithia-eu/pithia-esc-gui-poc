from django import forms

class ApiSpecificationUrlValidationForm(forms.Form):
    api_specification_url = forms.URLField()

class InlineMetadataValidationForm(forms.Form):
    xml_file_string = forms.CharField()
    xml_file_name = forms.CharField()

class InlineMetadataUpdateValidationForm(InlineMetadataValidationForm):
    existing_metadata_id = forms.CharField()