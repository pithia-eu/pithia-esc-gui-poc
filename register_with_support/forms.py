from django import forms
from django_countries import countries

class BaseEditorForm(forms.Form):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        for field in self.fields.values():
            if not 'class' in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})

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
        widget=forms.Textarea(attrs={
            'rows': '5',
        })
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
                'class': 'form-select',
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


class CitationDocumentationEditorFormComponent(forms.Form):
    citation_title = forms.CharField(
        label='Title of Documentation',
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

class LocationEditorFormComponent(forms.Form):
    MIN_POS_1 = -90
    MAX_POS_1 = 90
    MIN_POS_2 = -180
    MAX_POS_2 = 180
    
    def __init__(self, *args, crs_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['geometry_location_point_srs_name'].choices = crs_choices

    location_name = forms.CharField(
        label="Name",
        required=False,
        widget=forms.TextInput(),
        help_text='Geographic description of the location using text or an identifier.'
    )

    geometry_location_point_id = forms.CharField(
        label="Point ID",
        required=False,
        widget=forms.TextInput()
    )

    geometry_location_point_srs_name = forms.ChoiceField(
        label="SRS Name",
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    geometry_location_point_pos_1 = forms.FloatField(
        label="Pos",
        required=False,
        min_value=MIN_POS_1,
        max_value=MAX_POS_1,
        widget=forms.NumberInput(attrs={
            'min': MIN_POS_1,
            'max': MAX_POS_1,
        })
    )

    geometry_location_point_pos_2 = forms.FloatField(
        required=False,
        min_value=MIN_POS_2,
        max_value=MAX_POS_2,
        widget=forms.NumberInput(attrs={
            'min': MIN_POS_2,
            'max': MAX_POS_2,
        })
    )


class StatusEditorFormComponent(forms.Form):
    def __init__(self, *args, status_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = status_choices

    status = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
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
    CitationDocumentationEditorFormComponent,
    RelatedPartiesEditorFormComponent,
    StatusEditorFormComponent):
    def __init__(self, *args, **kwargs):
        super(ProjectEditorForm, self).__init__(*args, **kwargs)
        self.fields['description'].label = 'Additional Description'

    short_name = forms.CharField(
        label="Short Name",
        required=False,
        widget=forms.TextInput(),
        help_text='An acronym or abbreviation of the project\'s name.'
    )

    abstract = forms.CharField(
        label='Abstract',
        required=True,
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

class PlatformEditorForm(
    BaseEditorForm,
    CitationDocumentationEditorFormComponent,
    OrganisationEditorFormComponent,
    LocationEditorFormComponent,
    RelatedPartiesEditorFormComponent):

    def __init__(self, *args, type_choices=(), child_platform_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].choices = type_choices
        self.fields['child_platforms'].choices = child_platform_choices

    short_name = forms.CharField(
        label="Short Name",
        required=False,
        widget=forms.TextInput(),
        help_text='An acronym or abbreviation of the platform\'s name.'
    )

    type = forms.ChoiceField(
        label="Type",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    child_platforms = forms.MultipleChoiceField(
        label="Child Platforms",
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        })
    )

    url = forms.URLField(
        label="Link to Platform Website",
        required=False,
        widget=forms.URLInput()
    )

    standard_identifier_authority = forms.CharField(
        label='Authority',
        required=False,
        widget=forms.TextInput()
    )

    standard_identifier = forms.CharField(
        label='Value',
        required=False,
        widget=forms.TextInput()
    )

    standard_identifiers_json = forms.JSONField(
        required=False,
        widget=forms.HiddenInput()
    )

class OperationEditorForm(
    BaseEditorForm,
    OrganisationEditorFormComponent,
    CitationDocumentationEditorFormComponent,
    LocationEditorFormComponent,
    RelatedPartiesEditorFormComponent,
    StatusEditorFormComponent
):
    def __init__(self, *args, platform_choices=(), child_operation_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['platforms'].help_text = 'The operated platform(s).'
        self.fields['platforms'].choices = platform_choices
        self.fields['child_operations'].choices = child_operation_choices

    time_period_id = forms.CharField(
        label='ID',
        required=False,
        widget=forms.TextInput()
    )

    time_instant_begin_id = forms.CharField(
        label='ID',
        required=False,
        widget=forms.TextInput()
    )

    time_instant_begin_position = forms.DateField(
        label='Time Position',
        required=False,
        widget=forms.DateInput()
    )

    time_instant_end_id = forms.CharField(
        label='ID',
        required=False,
        widget=forms.TextInput()
    )

    time_instant_end_position = forms.DateField(
        label='Time Position',
        required=False,
        widget=forms.DateInput()
    )

    platforms = forms.MultipleChoiceField(
        label='Platforms',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select'
        })
    )

    child_operations = forms.MultipleChoiceField(
        label='Child Operations',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select'
        })
    )

class InstrumentEditorForm(
    BaseEditorForm,
    OrganisationEditorFormComponent,
    CitationDocumentationEditorFormComponent,
    RelatedPartiesEditorFormComponent
):
    def __init__(self, *args, instrument_type_choices=(), member_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].choices = instrument_type_choices
        self.fields['members'].choices = member_choices
    
    version = forms.FloatField(
        label='Version',
        required=False,
        widget=forms.NumberInput()
    )

    url = forms.URLField(
        label="Link to Instrument Website",
        required=False,
        widget=forms.URLInput()
    )
    
    type = forms.ChoiceField(
        label='Type',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    members = forms.MultipleChoiceField(
        label='Members',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        })
    )

    operational_mode_id = forms.CharField(
        label="ID",
        required=False,
        widget=forms.TextInput()
    )

    operational_mode_name = forms.CharField(
        label="Name",
        required=False,
        widget=forms.TextInput()
    )

    operational_mode_description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '4'
        })
    )

    operational_modes_json = forms.JSONField(
        required=False,
        widget=forms.HiddenInput()
    )