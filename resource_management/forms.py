from django import forms

from register.forms import (
    _API_DESCRIPTION_TEXTAREA_HELP_TEXT,
    UploadCatalogueDataSubsetFileForm,
)


_FILE_INPUT_LABEL = 'Updated Metadata File'


class UploadUpdatedFileForm(forms.Form):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    files = forms.FileField(
        label=_FILE_INPUT_LABEL,
        widget=forms.ClearableFileInput(attrs={
            'accept': 'application/xml',
            'class': 'form-control'
        })
    )

class UploadUpdatedDataCollectionFileForm(forms.Form):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    files = forms.FileField(
        label=_FILE_INPUT_LABEL,
        widget=forms.ClearableFileInput(attrs={
            'accept': 'application/xml',
            'class': 'form-control',
        })
    )

class UploadUpdatedCatalogueDataSubsetFileForm(UploadCatalogueDataSubsetFileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['files'].label = _FILE_INPUT_LABEL

class UpdateDataCollectionInteractionMethodsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    api_selected = forms.BooleanField(
        label='API',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    api_specification_url = forms.URLField(
        label='OpenAPI Specification URL',
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control'
        })
    )

    api_description = forms.CharField(
        label='Description',
        required=False,
        disabled=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
        help_text=_API_DESCRIPTION_TEXTAREA_HELP_TEXT
    )

class UpdateWorkflowOpenAPISpecificationURLForm(forms.Form):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    api_specification_url = forms.URLField(
        label='OpenAPI Specification URL',
        required=True,
        widget=forms.URLInput(attrs={
            'class': 'form-control'
        })
    )

    api_description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
        help_text=_API_DESCRIPTION_TEXTAREA_HELP_TEXT
    )