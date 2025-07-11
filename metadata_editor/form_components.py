import logging
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django_countries import countries
from phonenumber_field.formfields import PhoneNumberField


logger = logging.getLogger(__name__)


# Base components
class OrganisationSelect(forms.Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get('value'):
            option['attrs']['disabled'] = 'disabled'

        return option


class BaseEditorForm(forms.Form):
    required_css_class = 'required'

    def __init__(self, *args, form_metadata_type='', **kwargs):
        super().__init__(*args, **kwargs)
        self.form_metadata_type = form_metadata_type
        self.fields['name'].label = f'{self.form_metadata_type} {self.fields["name"].label}'
        self.label_suffix = ''
        for field in self.fields.values():
            if not 'class' in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})

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

    identifier_version = forms.CharField(
        label='Metadata Version',
        required=True,
        widget=forms.TextInput(),
        initial='1',
        help_text='The version number of the object being identified.'
    )


# Other components
class ContactInfoEditorFormComponent(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        email_addresses = cleaned_data.get('email_addresses_json')
        for email_address in email_addresses:
            try:
                validate_email(email_address)
            except ValidationError:
                logger.exception('Bad email')
                self.add_error('email_addresses_json', ValidationError(f'"{email_address}" is not a valid email.'))
                
        return cleaned_data

    phone = PhoneNumberField(
        label='Phone',
        required=False,
        widget=forms.TextInput(),
        help_text='Start the number with the country code - e.g. "+33" for phone numbers in France.'
    )

    delivery_point = forms.CharField(
        label='Street Name',
        required=False,
        widget=forms.TextInput()
    )

    city = forms.CharField(
        label='City',
        required=False,
        widget=forms.TextInput()
    )

    administrative_area = forms.CharField(
        label='County/State',
        required=False,
        widget=forms.TextInput()
    )

    postal_code = forms.CharField(
        label='Postal Code',
        required=False,
        widget=forms.TextInput()
    )

    country = forms.ChoiceField(
        label='Country',
        required=False,
        choices=(
            ('', ''),
            *((c.name, c.name) for c in countries)
        ),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    online_resource = forms.URLField(
        label='Link to Organisation Website',
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
        label='Contact Instructions',
        required=False,
        widget=forms.TextInput(),
        help_text='E.g. Contact by email or phone'
    )

    email_address = forms.EmailField(
        label='Email Address',
        required=False,
        widget=forms.EmailInput()
    )

    email_addresses_json = forms.JSONField(
        required=False,
        initial=list(),
        widget=forms.HiddenInput()
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
        help_text='Format: doi:10.nnnnnn/example'
    )

    other_citation_details = forms.CharField(
        label='Full Citation',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
        })
    )

    citation_linkage_url = forms.URLField(
        label='Link to Online Resource',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://'
        })
    )

    citations_json = forms.JSONField(
        required=False,
        initial=list(),
        widget=forms.HiddenInput()
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
        initial=list(),
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
        label='Name',
        required=False,
        widget=forms.TextInput(),
        help_text='Geographic description of the location using text or an identifier.'
    )

    geometry_location_point_id = forms.CharField(
        label='Point ID',
        required=False,
        widget=forms.TextInput()
    )

    geometry_location_point_srs_name = forms.ChoiceField(
        label='SRS Name',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    geometry_location_point_pos_1 = forms.FloatField(
        label='Latitude',
        required=False,
        min_value=MIN_POS_1,
        max_value=MAX_POS_1,
        widget=forms.NumberInput(attrs={
            'min': MIN_POS_1,
            'max': MAX_POS_1,
        }),
        help_text='Minimum: -90, Maximum: 90'
    )

    geometry_location_point_pos_2 = forms.FloatField(
        label='Longitude',
        required=False,
        min_value=MIN_POS_2,
        max_value=MAX_POS_2,
        widget=forms.NumberInput(attrs={
            'min': MIN_POS_2,
            'max': MAX_POS_2,
        }),
        help_text='Minimum: -180, Maximum: 180'
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
    def __init__(self, *args, data_quality_flag_choices=(), metadata_quality_flag_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_quality_flags'].choices = data_quality_flag_choices
        self.fields['metadata_quality_flags'].choices = metadata_quality_flag_choices

    data_quality_flags = forms.MultipleChoiceField(
        label='Data Quality Flags',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        })
    )

    metadata_quality_flags = forms.MultipleChoiceField(
        label='Metadata Quality Flags',
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
        vector_representation_choices=(),
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.fields['capability_coordinate_system'].choices = coordinate_system_choices
        self.fields['capability_dimensionality_instance'].choices = dimensionality_instance_choices
        self.fields['capability_dimensionality_timeline'].choices = dimensionality_timeline_choices
        self.fields['capability_observed_property'].choices = observed_property_choices
        self.fields['capability_qualifier'].choices = qualifier_choices
        self.fields['capability_units'].choices = unit_choices
        self.fields['capability_vector_representation'].choices = vector_representation_choices

    capability_name = forms.CharField(
        label='Name',
        required=False,
        widget=forms.TextInput(),
        help_text='Name of the capability (for internal use within PITHIA system)'
    )

    capability_observed_property = forms.ChoiceField(
        label='Observed Property',
        required=False,
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

    capability_cadence = forms.FloatField(
        label='Cadence',
        required=False,
        widget=forms.NumberInput(attrs={
            'step': '0.1'
        }),
        help_text='Temporal resolution of the observations, if regularly repetitive.'
    )

    capability_cadence_units = forms.ChoiceField(
        label='Cadence Unit',
        required=False,
        choices=(
            ('', ''),
            ('year', 'Year'),
            ('month', 'Month'),
            ('day', 'Day'),
            ('hour', 'Hour'),
            ('minute', 'Minute'),
            ('second', 'Second'),
        ),
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    capability_vector_representation = forms.MultipleChoiceField(
        label='Vector Representation',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        }),
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
        initial=list(),
        widget=forms.HiddenInput()
    )


class StandardIdentifierEditorFormComponent(forms.Form):
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
        initial=list(),
        widget=forms.HiddenInput()
    )


class TimePeriodDateTimeEditorFormComponent(forms.Form):
    time_instant_begin_position = forms.DateTimeField(
        label='Begin Time',
        required=False,
        widget=forms.DateTimeInput()
    )

    time_instant_end_position = forms.DateTimeField(
        label='End Time',
        required=False,
        widget=forms.DateTimeInput()
    )


class TimePeriodValidationEditorFormComponent(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        time_instant_begin_position = cleaned_data.get('time_instant_begin_position')
        time_instant_end_position = cleaned_data.get('time_instant_end_position')
        if not time_instant_begin_position:
            return cleaned_data
        if not time_instant_end_position:
            return cleaned_data
        if time_instant_begin_position <= time_instant_end_position:
            return cleaned_data
        self.add_error('time_instant_begin_position', ValidationError('The begin time cannot be later than the end time.'))
        return cleaned_data


class CapabilityLinkEditorFormComponent(StandardIdentifierEditorFormComponent):
    def __init__(self, *args, platform_choices=(), capability_set_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['capability_link_platform'].choices = platform_choices
        self.fields['capability_link_capabilities'].choices = capability_set_choices

    capability_link_platform = forms.MultipleChoiceField(
        label='Platform',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        })
    )

    capability_link_capabilities = forms.ChoiceField(
        label='',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    capability_link_standard_identifier_authority = forms.CharField(
        label='Authority',
        required=False,
        widget=forms.TextInput()
    )

    capability_link_standard_identifier = forms.CharField(
        label='Value',
        required=False,
        widget=forms.TextInput()
    )

    capability_link_standard_identifiers_json = forms.JSONField(
        required=False,
        initial=list(),
        widget=forms.HiddenInput()
    )

    capability_link_time_span_begin_position = forms.CharField(
        label='Begin Position',
        required=False,
        widget=forms.DateInput()
    )

    capability_link_time_span_end_position = forms.ChoiceField(
        label='End Position (Indeterminate)',
        required=False,
        choices=(
            ('', ''),
            ('after', 'After'),
            ('before', 'Before'),
            ('now', 'Now'),
            ('unknown', 'Unknown'),
        ),
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    capability_link_time_spans_json = forms.JSONField(
        required=False,
        initial=list(),
        widget=forms.HiddenInput()
    )

    capability_links_json = forms.JSONField(
        required=False,
        initial=list(),
        widget=forms.HiddenInput()
    )

class SourceMetadataFormComponent(forms.Form):
    def __init__(self, *args, data_format_choices=(), service_function_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source_data_formats'].choices = data_format_choices
        self.fields['source_service_functions'].choices = service_function_choices

    def clean_source_linkages(self, cleaned_data):
        sources = cleaned_data.get('sources_json')
        for source in sources:
            linkage = source.get('linkage')
            is_linkage_a_url = True
            is_linkage_an_email = True
            # Test if URL
            try:
                forms.URLField().clean(linkage)
            except ValidationError:
                is_linkage_a_url = False

            # Test if email
            try:
                forms.EmailField().clean(linkage)
            except ValidationError:
                is_linkage_an_email = False

            if is_linkage_a_url or is_linkage_an_email:
                continue
            self.add_error('sources_json', ValidationError('One or multiple online resource links are invalid.'))

    def clean(self):
        cleaned_data = super().clean()
        self.clean_source_linkages(cleaned_data)
        return cleaned_data

    source_service_functions = forms.MultipleChoiceField(
        required=False,
        label='Service Function',
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        }),
        help_text='The function performed by the online resource. E.g. Direct data download. Obtained from a controlled vocabulary.'
    )

    source_linkage = forms.CharField(
        required=False,
        label='Link to Online Resource',
        widget=forms.TextInput(attrs={
            'placeholder': 'https://',
        }),
        help_text='A location (address) for online access using a Uniform Resource Locator/Uniform Resource Identifier address.'
    )

    source_file = forms.FileField(
        required=False,
        label='File',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        })
    )

    source_name = forms.CharField(
        required=False,
        label='Name',
        widget=forms.TextInput(),
        help_text='Name of the online resource.'
    )

    source_protocol = forms.CharField(
        required=False,
        label='Protocol',
        widget=forms.TextInput(),
        help_text='The connection protocol e.g. http, ftp, file.'
    )

    source_description = forms.CharField(
        required=False,
        label='Description',
        widget=forms.Textarea(attrs={
            'rows': 3,
        }),
        help_text='A text description of what the online resource is/does.'
    )

    source_data_formats = forms.MultipleChoiceField(
        required=False,
        label='Data Formats',
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        }),
        help_text='The format of the stored result accessible from the online resource. This property references a term, e.g. NetCDF, from a controlled vocabulary.'
    )

    sources_json = forms.JSONField(
        required=False,
        initial=list(),
        widget=forms.HiddenInput()
    )


class FeaturesOfInterestMetadataFormComponent(forms.Form):
    def __init__(self, *args, feature_of_interest_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['features_of_interest'].choices = feature_of_interest_choices

    features_of_interest = forms.MultipleChoiceField(
        label='Features of Interest (Named Regions)',
        required=True,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        }),
        help_text='Space region which is the feature of the interest of the observation or a sampled feature. This attribute takes values from a controlled vocabulary. '
    )