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

    register_doi = forms.BooleanField(
        label='Generate a DOI for this Data Subset',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
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

    details_file_storage_method = forms.ChoiceField(
        label='Upload your workflow details file here',
        choices=(
            ('datahub', 'I will upload a file now.'),
            ('external', 'I will provide a link in the metadata file.'),
        ),
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-check-input',
            }
        ),
        initial='datahub'
    )

    is_details_file_input_used = forms.ChoiceField(
        label='I will upload a details file now',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        ),
        initial=True
    )

    details_file = forms.FileField(
        label='Select Your Workflow Details File',
        widget=forms.ClearableFileInput(attrs={
            'accept': 'application/pdf',
            'class': 'form-control',
        }),
        help_text='Allowed formats: PDF'
    )