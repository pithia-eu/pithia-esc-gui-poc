from django import forms
from django_countries import countries

class BaseEditorForm(forms.Form):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        for visible in self.visible_fields():
            if not isinstance(visible.field.widget, forms.Select):
                visible.field.widget.attrs['class'] = 'form-control'

    localid = forms.CharField(
        label='Local ID',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-secondary-emphasis bg-body-secondary',
            'readonly': True,
        }),
        help_text=f'A basic local ID is automatically generated using this registration\'s full name. If this is local ID is already in use, a more complex local ID will be generated.'
    )

    namespace = forms.CharField(
        label='Namespace',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-secondary-emphasis bg-body-secondary',
            'readonly': True,
        }),
        help_text=f'This is automatically generated with the short name of the selected organisation.'
    )

    name = forms.CharField(
        label='Full Name',
        required=True,
        widget=forms.TextInput()
    )

    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea()
    )


class OrganisationSelect(forms.Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get('value'):
            option['attrs']['disabled'] = 'disabled'

        return option

class OrganisationEditorFormComponent(forms.Form):
    def __init__(self, *args, organisation_choices=(), **kwargs):
        super(OrganisationEditorFormComponent, self).__init__(*args, **kwargs)
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


class ContactInfoEditorFormComponent(forms.Form):
    phone = forms.CharField(
        label="Phone",
        required=False,
        widget=forms.TextInput(),
        help_text='Start the number with the country code - e.g. "+33" for phone numbers in France.'
    )

    delivery_point = forms.CharField(
        label="Street Name",
        required=False,
        widget=forms.TextInput()
    )

    city = forms.CharField(
        label="City",
        required=False,
        widget=forms.TextInput()
    )

    administrative_area = forms.CharField(
        label="County/State",
        required=False,
        widget=forms.TextInput()
    )

    postal_code = forms.CharField(
        label="Postal Code",
        required=False,
        widget=forms.TextInput()
    )

    country = forms.ChoiceField(
        label='Country',
        required=False,
        choices=((c.name, c.name) for c in countries),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    online_resource = forms.URLField(
        label="Link to Organisation Website",
        required=False,
        widget=forms.URLInput()
    )

    hours_of_service_start = forms.TimeField(
        required=False,
        widget=forms.TimeInput()
    )

    hours_of_service_end = forms.TimeField(
        required=False,
        widget=forms.TimeInput()
    )

    contact_instructions = forms.CharField(
        label="Contact Instructions",
        required=False,
        widget=forms.TextInput(),
        help_text='E.g. Contact by email or phone'
    )

    email_address = forms.EmailField(
        label="Email Address",
        required=False,
        widget=forms.EmailInput()
    )


class ProjectDocumentationEditorFormComponent(forms.Form):
    citation_title = forms.CharField(
        label='Title',
        required=False,
        widget=forms.TextInput()
    )

    citation_publication_date = forms.CharField(
        label='Publication Date',
        required=False,
        widget=forms.DateInput()
    )

    citation_doi = forms.CharField(
        label='DOI',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'doi:10.xxxxx'
        })
    )

    other_citation_details = forms.CharField(
        label='Full Citation',
        required=False,
        widget=forms.Textarea()
    )

    citation_linkage_url = forms.URLField(
        label='Link to Online Resource',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://'
        })
    )


class RelatedPartiesEditorFormComponent(forms.Form):
    def __init__(self, *args, related_party_role_choices=(), related_party_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_party'].choices = related_party_choices
        self.fields['related_party_role'].choices = related_party_role_choices

    related_party_role = forms.ChoiceField(
        label='Role',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    related_party = forms.MultipleChoiceField(
        label='Parties',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        })
    )

    related_parties_json = forms.JSONField(
        required=False,
        widget=forms.HiddenInput()
    )


class OrganisationEditorForm(BaseEditorForm, ContactInfoEditorFormComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['localid'].help_text = f'A basic local ID is automatically generated using this organisation\'s short name. If there is another organisation sharing the same short name, a more complex local ID will be generated.'
        self.fields['namespace'].widget = forms.HiddenInput()

    short_name = forms.CharField(
        label="Short Name",
        required=True,
        widget=forms.TextInput(),
        help_text='This will be used to automatically generate this registration\'s local ID suffix and will also be used as the namespace for future registrations associated with this organisation.'
    )


class IndividualEditorForm(BaseEditorForm, ContactInfoEditorFormComponent, OrganisationEditorFormComponent):
    def __init__(self, *args, **kwargs):
        super(IndividualEditorForm, self).__init__(*args, **kwargs)
        self.fields['online_resource'].label = 'Link to Organisation Website/Staff Page'


class ProjectEditorForm(
    BaseEditorForm,
    OrganisationEditorFormComponent,
    ProjectDocumentationEditorFormComponent,
    RelatedPartiesEditorFormComponent):
    def __init__(self, *args, status_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = status_choices

    short_name = forms.CharField(
        label="Short Name",
        required=False,
        widget=forms.TextInput(),
        help_text='An acronym or abbreviation of the project\'s name.'
    )

    abstract = forms.CharField(
        label='Abstract',
        required=False,
        widget=forms.Textarea()
    )

    url = forms.URLField(
        label="Link to Project Website",
        required=False,
        widget=forms.URLInput()
    )

    # Following keyword-related fields are only used to help render form
    keyword_type_code = forms.CharField(
        label='Keyword Type Code',
        required=False,
        widget=forms.TextInput()
    )

    keyword_type = forms.CharField(
        label='Keyword Type',
        required=False,
        widget=forms.TextInput()
    )

    keyword = forms.CharField(
        label='Keywords',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
        })
    )

    # Only keyword-related field that gets processed
    keywords_json = forms.JSONField(
        required=False,
        widget=forms.HiddenInput()
    )

    status = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )