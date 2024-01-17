from django import forms


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
    files = MultipleFileField(
        label='Metadata File(s)',
    )


class UploadDataCollectionFileForm(forms.Form):
    files = forms.FileField(
        label='Metadata File',
        widget=forms.ClearableFileInput(attrs={
            'accept': 'application/xml',
            'class': 'form-control',
        }))
    api_selected = forms.BooleanField(
        label='API',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    api_specification_url = forms.CharField(
        label='Link to API Specification',
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={
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
            'style': 'resize: none;'
        })
    )

class UploadWorkflowFileForm(forms.Form):
    files = forms.FileField(
        label='Metadata file',
        widget=forms.ClearableFileInput(attrs={
            'accept': 'application/xml',
            'class': 'form-control',
        })
    )
    api_specification_url = forms.CharField(
        label='Workflow OpenAPI Specification URL',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )


class UploadCatalogueDataSubsetFileForm(forms.Form):
    files = forms.FileField(
        label='Metadata File',
        widget=forms.ClearableFileInput(attrs={
            'accept': 'application/xml',
            'class': 'form-control',
        })
    )

    register_doi = forms.BooleanField(
        label='Generate DOI for this Data Subset',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
