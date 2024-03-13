from django import forms
from django_countries import countries

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
        help_text=f'A basic local ID is automatically generated using this registration\'s full name. If this is taken, a more complex local ID will be generated.'
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

    country = forms.ChoiceField(
        label='Country',
        required=False,
        choices=((c.name, c.name) for c in countries),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    online_resource = forms.CharField(
        label="Link to Organisation Website",
        required=False,
        widget=forms.URLInput(attrs={
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
        self.fields['localid'].help_text = f'A basic local ID is automatically generated using this organisation\'s short name. A more complex local ID will be generated if there is another organisation sharing the same short name.'
        self.fields['namespace'].widget = forms.HiddenInput()

    short_name = forms.CharField(
        label="Short Name",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        help_text='This will be used to automatically generate this registration\'s local ID suffix and will be also used as the namespace for future registrations associated with this organisation.'
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