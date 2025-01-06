from django import forms


_FILE_INPUT_MULTIPLE_LABEL = 'Metadata File/Files'
_FILE_INPUT_LABEL = 'Metadata File'
_API_DESCRIPTION_TEXTAREA_HELP_TEXT = 'E.g. a brief description of what the API can do'


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={
            'accept': 'application/xml',
            'class': 'form-control',
            'multiple': 'true',
        }))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class UploadFileForm(forms.Form):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    files = MultipleFileField(
        label=_FILE_INPUT_MULTIPLE_LABEL,
    )


class UploadDataCollectionFileForm(forms.Form):
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
        disabled=True,
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


class UploadCatalogueDataSubsetFileForm(forms.Form):
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

    online_resource_file = forms.FileField(
        label='Online Resource File',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
        })
    )

    register_doi = forms.BooleanField(
        label='Generate a DOI for this Data Subset',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    is_file_uploaded_for_each_online_resource = forms.BooleanField(
        label='Use Files for Each Online Resource',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'role': 'switch',
        }),
        help_text='Toggle whether you would like these online resources to link to files uploaded to the e-Science Centre, or to external webpages.',
        initial=True
    )


class WorkflowOpenAPISpecificationForm(forms.Form):
    required_css_class = 'required'

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


class UploadWorkflowFileForm(WorkflowOpenAPISpecificationForm):
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

    is_workflow_details_file_input_used = forms.BooleanField(
        label='I will upload a details file now',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        ),
        initial=True
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