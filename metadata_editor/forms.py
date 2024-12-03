from django import forms

from .form_components import *


class OrganisationEditorForm(BaseEditorForm, ContactInfoEditorFormComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['short_name'].label = f'{self.form_metadata_type} {self.fields["short_name"].label}'

    short_name = forms.CharField(
        label='Short Name',
        required=True,
        widget=forms.TextInput(),
        help_text='This will be used as the namespace for future registrations associated with this organisation.'
    )


class IndividualEditorForm(BaseEditorForm, ContactInfoEditorFormComponent):
    def __init__(self, *args, **kwargs):
        super(IndividualEditorForm, self).__init__(*args, **kwargs)
        self.fields['online_resource'].label = 'Link to Organisation Website/Staff Page'

    position_name = forms.CharField(
        label='Position Name',
        required=False,
        widget=forms.TextInput(),
        help_text='Role of the individual within the organisation.'
    )


class ProjectEditorForm(
    BaseEditorForm,
    CitationDocumentationEditorFormComponent,
    RelatedPartiesEditorFormComponent,
    StatusEditorFormComponent):
    def __init__(self, *args, **kwargs):
        super(ProjectEditorForm, self).__init__(*args, **kwargs)
        self.fields['short_name'].label = f'{self.form_metadata_type} {self.fields["short_name"].label}'
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
        initial=list,
        widget=forms.HiddenInput()
    )

    keywords_extra_json = forms.JSONField(
        required=False,
        initial=dict,
        widget=forms.HiddenInput()
    )


class PlatformEditorForm(
    BaseEditorForm,
    CitationDocumentationEditorFormComponent,
    LocationEditorFormComponent,
    RelatedPartiesEditorFormComponent):

    def __init__(self, *args, type_choices=(), child_platform_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['short_name'].label = f'{self.form_metadata_type} {self.fields["short_name"].label}'
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
        initial=list,
        widget=forms.HiddenInput()
    )

    standard_identifiers_extra_json = forms.JSONField(
        required=False,
        initial=dict,
        widget=forms.HiddenInput()
    )


class OperationEditorForm(
    BaseEditorForm,
    CitationDocumentationEditorFormComponent,
    LocationEditorFormComponent,
    RelatedPartiesEditorFormComponent,
    StatusEditorFormComponent,
    TimePeriodEditorFormComponent
):
    def __init__(self, *args, platform_choices=(), child_operation_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['platforms'].help_text = 'The operated platform(s).'
        self.fields['platforms'].choices = platform_choices
        self.fields['child_operations'].choices = child_operation_choices

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
    CitationDocumentationEditorFormComponent,
    RelatedPartiesEditorFormComponent
):
    def __init__(self, *args, instrument_type_choices=(), member_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].choices = instrument_type_choices
        self.fields['members'].choices = member_choices
    
    version = forms.CharField(
        label='Instrument Version',
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
        initial=list,
        widget=forms.HiddenInput()
    )

    operational_modes_extra_json = forms.JSONField(
        required=False,
        initial=dict,
        widget=forms.HiddenInput()
    )


class AcquisitionCapabilitiesEditorForm(
    BaseEditorForm,
    CapabilitiesFormComponent,
    CitationDocumentationEditorFormComponent,
    DataLevelFormComponent,
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

    input_name = forms.CharField(
        label='Name',
        required=False,
        widget=forms.TextInput()
    )

    input_description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '5',
        })
    )

    input_descriptions_json = forms.JSONField(
        required=False,
        initial=list,
        widget=forms.HiddenInput()
    )

    input_descriptions_extra_json = forms.JSONField(
        required=False,
        initial=dict,
        widget=forms.HiddenInput()
    )


class AcquisitionEditorForm(
    BaseEditorForm,
    CapabilityLinkEditorFormComponent,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['capability_link_capabilities'].label = 'Acquisition Capabilities'


class ComputationCapabilitiesEditorForm(
    BaseEditorForm,
    CapabilitiesFormComponent,
    CitationDocumentationEditorFormComponent,
    DataLevelFormComponent,
    QualityAssessmentFormComponent,
    RelatedPartiesEditorFormComponent
):
    def __init__(self, *args, child_computation_choices=(), computation_type_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['child_computations'].choices = child_computation_choices
        self.fields['type'].choices = computation_type_choices

    type = forms.MultipleChoiceField(
        label='Type',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        })
    )

    version = forms.CharField(
        label='Computation Component Version',
        required=False,
        widget=forms.TextInput()
    )

    processing_input_name = forms.CharField(
        label='Name',
        required=False,
        widget=forms.TextInput()
    )

    processing_input_description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3
        })
    )

    processing_inputs_json = forms.JSONField(
        required=False,
        initial=list,
        widget=forms.HiddenInput()
    )

    processing_inputs_extra_json = forms.JSONField(
        required=False,
        initial=dict,
        widget=forms.HiddenInput()
    )

    child_computations = forms.MultipleChoiceField(
        label='Child Computations',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        })
    )

    software_reference_citation_title = forms.CharField(
        label='Title of Documentation',
        required=False,
        widget=forms.TextInput()
    )

    software_reference_citation_publication_date = forms.CharField(
        label='Publication Date',
        required=False,
        widget=forms.DateInput()
    )

    software_reference_citation_doi = forms.CharField(
        label='DOI',
        required=False,
        widget=forms.TextInput(attrs={
            'pattern': 'doi:10.[0-9]{4,}(?:[.][0-9]+)*/.+'
        }),
        help_text='Format: doi:10.nnnnnn/example'
    )

    software_reference_other_citation_details = forms.CharField(
        label='Full Citation',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
        })
    )

    software_reference_citation_linkage_url = forms.URLField(
        label='Link to Online Resource',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://'
        })
    )


class ComputationEditorForm(
    BaseEditorForm,
    CapabilityLinkEditorFormComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['capability_link_capabilities'].label = 'Computation Capabilities'


class ProcessEditorForm(
    BaseEditorForm,
    CapabilitiesFormComponent,
    CitationDocumentationEditorFormComponent,
    DataLevelFormComponent,
    QualityAssessmentFormComponent,
    RelatedPartiesEditorFormComponent):
    def __init__(self, *args, acquisition_choices=(), computation_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['acquisitions'].choices = acquisition_choices
        self.fields['computations'].choices = computation_choices

    acquisitions = forms.MultipleChoiceField(
        label='Acquisition Components',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        }),
        help_text='A component of acquisition type.'
    )

    computations = forms.MultipleChoiceField(
        label='Computation Components',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        }),
        help_text='A component of computation type.'
    )


class DataCollectionEditorForm(
    BaseEditorForm,
    DataLevelFormComponent,
    QualityAssessmentFormComponent,
    RelatedPartiesEditorFormComponent,
    SourceMetadataFormComponent):
    def __init__(
            self,
            *args,
            type_choices=(),
            project_choices=(),
            sub_collection_choices=(),
            feature_of_interest_choices=(),
            permission_choices=(),
            process_choices=(),
            **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['types'].choices = type_choices
        self.fields['projects'].choices = project_choices
        self.fields['sub_collections'].choices = sub_collection_choices
        self.fields['features_of_interest'].choices = feature_of_interest_choices
        self.fields['permissions'].choices = permission_choices
        self.fields['process'].choices = process_choices
        self.fields['source_linkage'].required = True
        self.fields['source_name'].required = True
        self.fields['source_protocol'].required = True

    types = forms.MultipleChoiceField(
        label='Types',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        }),
        help_text='Type of the data collection (instrument or model) from a controlled vocabulary.'
    )

    projects = forms.MultipleChoiceField(
        label='Projects',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        }),
        help_text='Project(s) that the data collection belongs to.'
    )

    sub_collections = forms.MultipleChoiceField(
        label='Sub-collections',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        }),
        help_text='Sub-collection of the collection.'
    )

    features_of_interest = forms.MultipleChoiceField(
        label='Features of Interest (Named Regions)',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        }),
        help_text='Space region which is the feature of the interest of the observation or a sampled feature. This attribute takes values from a controlled vocabulary. '
    )

    permissions = forms.MultipleChoiceField(
        label='Permissions',
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
        }),
        help_text='''Restrictions on the access and use of the observation\'s result.
                    These are known without navigating from the observation to the result.'''
    )

    process = forms.ChoiceField(
        label='Procedure',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='The process used to generate the result.'
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
        })
    )


class CatalogueEditorForm(BaseEditorForm):
    def __init__(self, *args, catalogue_category_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['catalogue_category'].choices = catalogue_category_choices

    catalogue_category = forms.ChoiceField(
        label='Catalogue Category',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='A category of the catalogue from the ontology disctionary.'
    )


class CatalogueEntryEditorForm(
    BaseEditorForm,
    TimePeriodEditorFormComponent):
    def __init__(self, *args, catalogue_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['catalogue_identifier'].choices = catalogue_choices
        self.fields['description'].help_text = 'A free-text description of the catalogue entry contents.'
        self.fields['time_period_id'].required = True
        self.fields['time_instant_begin_id'].required = True
        self.fields['time_instant_end_id'].required = True

    catalogue_identifier = forms.ChoiceField(
        label='Catalogue',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='The catalogue that this entry belongs to.'
    )

    time_instant_begin_position = forms.DateTimeField(
        label='Time Position',
        required=True,
        widget=forms.DateTimeInput()
    )

    time_instant_end_position = forms.DateTimeField(
        label='Time Position',
        required=True,
        widget=forms.DateTimeInput()
    )


class CatalogueDataSubsetForm(
    BaseEditorForm,
    DataLevelFormComponent,
    QualityAssessmentFormComponent,
    SourceMetadataFormComponent,
    TimePeriodEditorFormComponent):
    def __init__(self, *args, data_collection_choices=(), catalogue_entry_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_collection'].choices = data_collection_choices
        self.fields['entry_identifier'].choices = catalogue_entry_choices
        self.fields['description'].help_text = 'A free-text description of the data subset contents.'
        self.fields['time_period_id'].required = True
        self.fields['time_instant_begin_id'].required = True
        self.fields['time_instant_end_id'].required = True
        self.fields['data_quality_flags'].required = True

    data_collection = forms.ChoiceField(
        label='Subset of Data Collection',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='The PITHIA Data Collection that holds metadata for this subset.'
    )

    entry_identifier = forms.ChoiceField(
        label='Catalogue Entry',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='The catalogue entry that this data subset belongs to.'
    )

    time_instant_begin_position = forms.DateTimeField(
        label='Time Position',
        required=True,
        widget=forms.DateTimeInput()
    )

    time_instant_end_position = forms.DateTimeField(
        label='Time Position',
        required=True,
        widget=forms.DateTimeInput()
    )

    data_levels = forms.ChoiceField(
        label='Data Level',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    register_doi = forms.BooleanField(
        label='Generate a DOI for this Data Subset',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )

    is_file_uploaded_for_each_online_resource = forms.BooleanField(
        label='Upload files for online resources',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'role': 'switch',
        }),
        initial=True
    )


class WorkflowEditorForm(BaseEditorForm):
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
        label='Workflow Details URL',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://',
            'disabled': 'true',
        }),
        help_text='The link must point directly to the details file.'
    )

    workflow_details_file = forms.FileField(
        label='Workflow Details File',
        required=False,
        widget=forms.FileInput(attrs={
            'accept': 'application/pdf',
            'placeholder': 'https://',
        }),
        help_text='Accepted formats: PDF'
    )

    workflow_details_file_source = forms.ChoiceField(
        label='Workflow Details Format',
        required=True,
        choices=(
            ('file_upload', 'File Upload'),
            ('external', 'Link to the Workflow Details File')
        ),
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        })
    )