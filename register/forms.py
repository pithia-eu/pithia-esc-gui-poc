from django import forms

from common.models import Organisation


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    files = MultipleFileField(
        label='Upload Your Metadata File(s)',
    )


class UploadDataCollectionFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    files = forms.FileField(
        label='Upload Your Metadata File',
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

    api_specification_url = forms.CharField(
        label='OpenAPI Specification URL',
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
        })
    )


class UploadCatalogueDataSubsetFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    files = forms.FileField(
        label='Upload Your Metadata File',
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


class UploadWorkflowFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    files = forms.FileField(
        label='Upload Your Metadata File',
        widget=forms.ClearableFileInput(attrs={
            'accept': 'application/xml',
            'class': 'form-control',
        })
    )

    api_specification_url = forms.CharField(
        label='OpenAPI Specification URL',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    api_description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        })
    )


# Metadata input support
class BaseInputSupportForm(forms.Form):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    localid = forms.CharField(
        label='Local ID',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'disabled': True,
        }),
        help_text=f'This is automatically generated using the name of this registration.'
    )

    namespace = forms.CharField(
        label='Namespace',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'disabled': True,
        }),
        help_text=f'This is automatically generated with the short name of the selected organisation.'
    )

    name = forms.CharField(
        label='Full Name',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )

class ContactInfoInputSupportForm(BaseInputSupportForm):
    phone = forms.CharField(
        label="Phone",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        help_text='Start the number with the country code - e.g. "+33" for phone numbers in France.'
    )

    delivery_point = forms.CharField(
        label="Street Name",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    city = forms.CharField(
        label="City",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    administrative_area = forms.CharField(
        label="County/State",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    postal_code = forms.CharField(
        label="Postal Code",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    country = forms.CharField(
        label='Country',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    online_resource = forms.CharField(
        label="Link to Organisation Website",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    hours_of_service_start = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    hours_of_service_end = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    contact_instructions = forms.CharField(
        label="Contact Instructions",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        help_text='E.g. Contact by email or phone'
    )

    email_address = forms.EmailField(
        label="Email Address",
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )

class OrganisationInputSupportForm(ContactInfoInputSupportForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['localid'].help_text = None
        self.fields['namespace'].widget = forms.HiddenInput()

    short_name = forms.CharField(
        label="Short Name",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        help_text='This will be used to automatically generate this registration\'s local ID suffix as well as the namespace for future registrations associated with this organisation.'
    )

class OrganisationSelect(forms.Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get('value'):
            option['attrs']['disabled'] = 'disabled'

        return option

class IndividualInputSupportForm(ContactInfoInputSupportForm):
    def __init__(self, *args, organisation_choices=(), **kwargs):
        super(IndividualInputSupportForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['online_resource'].label = 'Link to Organisation Website/Staff Page'
        self.fields['organisation'].choices = organisation_choices

    organisation = forms.ChoiceField(
        choices=(),
        label='Organisation',
        required=True,
        widget=OrganisationSelect(
            attrs={
                'class': 'form-select'
            }
        ),
        help_text='The chosen organisation\'s short name will be used as this registration\'s namespace.'
    )