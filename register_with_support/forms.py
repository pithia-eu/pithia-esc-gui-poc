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
            'pattern': 'doi:10.[0-9]{4,}(?:[.][0-9]+)*/.+'
        }),
        help_text='Format: doi:10.xxxxx'
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

class QualityAssessmentFormComponent(forms.Form):
    def __init__(self, *args, quality_assessment_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quality_assessments'].choices = quality_assessment_choices

    quality_assessments = forms.MultipleChoiceField(
        label='Quality Assessment',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        })
    )

class DataLevelFormComponent(forms.Form):
    def __init__(self, *args, data_level_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_levels'].choices = data_level_choices

    data_levels = forms.MultipleChoiceField(
        label='Data Levels',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        })
    )

class CapabilitiesFormComponent(forms.Form):
    def __init__(
        self,
        *args,
        coordinate_system_choices=(),
        dimensionality_instance_choices=(),
        dimensionality_timeline_choices=(),
        observed_property_choices=(),
        qualifier_choices=(),
        unit_choices=(),
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.fields['capability_coordinate_system'].choices = coordinate_system_choices
        self.fields['capability_dimensionality_instance'].choices = dimensionality_instance_choices
        self.fields['capability_dimensionality_timeline'].choices = dimensionality_timeline_choices
        self.fields['capability_observed_property'].choices = observed_property_choices
        self.fields['capability_qualifier'].choices = qualifier_choices
        self.fields['capability_units'].choices = unit_choices

    capability_name = forms.CharField(
        label='Name',
        required=True,
        widget=forms.TextInput(),
        help_text='Name of the capability (for internal use within PITHIA system)'
    )

    capability_observed_property = forms.ChoiceField(
        label='Observed Property',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='What the process can measure or predict'
    )

    capability_dimensionality_instance = forms.ChoiceField(
        label='Dimensionality Instance',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='The data domain of the single instance'
    )

    capability_dimensionality_timeline = forms.ChoiceField(
        label='Dimensionality Timeline',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='For animation...'
    )

    capability_cadence = forms.CharField(
        label='Cadence',
        required=False,
        widget=forms.TextInput(),
        help_text='Temporal resolution of the observations, if regularly repetitive.'
    )

    capability_vector_representation = forms.CharField(
        label='Vector Representation',
        required=False,
        widget=forms.TextInput(),
        help_text='For those capabilities that are limited in their representation of the vector (i.e., only projections or components).'
    )

    capability_coordinate_system = forms.ChoiceField(
        label='Co-ordinate System',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='System of coordinates for the vector representations from PITHIA ontology vocabulary.'
    )

    capability_units = forms.ChoiceField(
        label='Units',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='Units of the observed property.'
    )

    capability_qualifier = forms.MultipleChoiceField(
        label='Qualifier',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        }),
        help_text='Qualifier of the capability to observe the property (dictionary-controlled).'
    )

    capabilities_json = forms.JSONField(
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
    
    version = forms.CharField(
        label='Version',
        required=False,
        widget=forms.TextInput()
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
        }),
        help_text='Member of a group of instruments.'
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
            'rows': '1',
        })
    )

    operational_modes_json = forms.JSONField(
        required=False,
        widget=forms.HiddenInput()
    )

class AcquisitionCapabilitiesEditorForm(
    BaseEditorForm,
    CapabilitiesFormComponent,
    CitationDocumentationEditorFormComponent,
    DataLevelFormComponent,
    OrganisationEditorFormComponent,
    QualityAssessmentFormComponent,
    RelatedPartiesEditorFormComponent
):
    def __init__(self, *args, instrument_choices=(), operational_mode_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instrument_mode_pair_instrument'].choices = instrument_choices
        self.fields['instrument_mode_pair_mode'].choices = operational_mode_choices

    instrument_mode_pair_instrument = forms.ChoiceField(
        label='Instrument',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    instrument_mode_pair_mode = forms.ChoiceField(
        label='Mode',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'disabled': 'true',
        })
    )

    input_description = forms.CharField(
        label='Input Description',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '5',
        })
    )

    output_description = forms.CharField(
        label='Output Description',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '5',
        })
    )


class WorkflowEditorForm(BaseEditorForm, OrganisationEditorFormComponent):
    def __init__(self, *args, data_collection_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_collection_1'].choices = data_collection_choices
        self.fields['data_collection_2_and_others'].choices = data_collection_choices

    data_collection_1 = forms.ChoiceField(
        label='Data Collection 1',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    data_collection_2_and_others = forms.MultipleChoiceField(
        label='Data Collection 2 and others',
        required=True,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        })
    )

    workflow_details = forms.URLField(
        label='Link to Workflow Details',
        required=True,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://',
        })
    )