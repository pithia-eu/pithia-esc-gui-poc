from django import forms

from register.forms import (
    _API_DESCRIPTION_TEXTAREA_HELP_TEXT,
    UploadDataSubsetFileForm,
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


class UploadUpdatedDataSubsetFileForm(UploadDataSubsetFileForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['files'].label = _FILE_INPUT_LABEL

    is_existing_datahub_file_used = forms.BooleanField(
        label='Use existing file with the same name as this online resource',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        initial=True
    )

    online_resource_datahub_file_usage = forms.JSONField(
        required=False,
        widget=forms.HiddenInput(),
        initial=dict()
    )


class UploadUpdatedWorkflowFileForm(UploadUpdatedFileForm):
    workflow_details_file_source = forms.ChoiceField(
        label='Workflow Details File Source',
        required=True,
        choices=(
            ('existing', 'Keep Using the Same File'),
            ('file_upload', 'Upload a New Workflow Details File'),
            ('external', 'Use the Workflow Details File Link in the Metadata File'),
        ),
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        })
    )

    workflow_details_file = forms.FileField(
        label='Select Your Workflow Details File',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'accept': 'application/pdf',
            'class': 'form-control',
        }),
        help_text='Allowed formats: PDF'
    )


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