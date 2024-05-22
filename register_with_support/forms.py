from django import forms
from .form_components import *


class OrganisationEditorForm(BaseEditorForm, ContactInfoEditorFormComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['short_name'].label = f'{self.form_metadata_type} {self.fields["short_name"].label}'
        self.fields['localid'].help_text = f'A basic local ID is automatically generated using this organisation\'s short name. If there is another organisation sharing the same short name, a more complex local ID will be generated.'
        self.fields['namespace'].widget = forms.HiddenInput()

    short_name = forms.CharField(
        label='Short Name',
        required=True,
        widget=forms.TextInput(),
        help_text='This will be used to automatically generate this registration\'s local ID suffix and will also be used as the namespace for future registrations associated with this organisation.'
    )


class IndividualEditorForm(BaseEditorForm, ContactInfoEditorFormComponent):
    def __init__(self, *args, **kwargs):
        super(IndividualEditorForm, self).__init__(*args, **kwargs)
        self.fields['online_resource'].label = 'Link to Organisation Website/Staff Page'


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

class OperationEditorForm(
    BaseEditorForm,
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
        initial=list,
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

    # output_name = forms.CharField(
    #     label='Name',
    #     required=False,
    #     widget=forms.TextInput()
    # )

    # output_description = forms.CharField(
    #     label='Description',
    #     required=False,
    #     widget=forms.Textarea(attrs={
    #         'rows': '5',
    #     })
    # )


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
        label='Version',
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

    processing_output_name = forms.CharField(
        label='Name',
        required=False,
        widget=forms.TextInput()
    )

    processing_output_description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3
        })
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
        help_text='Format: doi:10.xxxxx'
    )

    software_reference_other_citation_details = forms.CharField(
        label='Full Citation',
        required=False,
        widget=forms.Textarea()
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
        label='Link to Workflow Details',
        required=True,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://',
        })
    )