from django import forms

from metadata_editor.form_components import OrganisationSelect
from metadata_editor.forms import (
    AcquisitionCapabilitiesEditorForm,
    AcquisitionEditorForm,
    CatalogueEditorForm,
    DataSubsetForm,
    StaticDatasetEntryEditorForm,
    ComputationCapabilitiesEditorForm,
    ComputationEditorForm,
    DataCollectionEditorForm,
    IndividualEditorForm,
    InstrumentEditorForm,
    OperationEditorForm,
    OrganisationEditorForm,
    PlatformEditorForm,
    ProcessEditorForm,
    ProjectEditorForm,
    WorkflowEditorForm,
)
from register.forms import WorkflowOpenAPISpecificationForm


class EditorRegistrationForm(forms.Form):
    def __init__(self, *args, organisation_choices=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organisation'].label = f'Organisation Associated With the {self.form_metadata_type}'
        self.fields['organisation'].choices = organisation_choices

    localid = forms.CharField(
        label='Local ID',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-body-secondary-emphasis bg-body-secondary',
            'readonly': True,
        }),
        help_text='''The local ID is automatically generated from the full name you give this registration.
        It must be unique, so if the local ID generated has already been taken a timestamp will be added to
        help ensure uniqueness. The local ID also cannot be changed once this form is submitted.'''
    )

    namespace = forms.CharField(
        label='Namespace',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-body-secondary-emphasis bg-body-secondary',
            'readonly': True,
        }),
        help_text=f'This is automatically generated with the short name of the organisation associated with this registration.'
    )

    organisation = forms.ChoiceField(
        choices=(),
        label='Organisation',
        required=True,
        widget=OrganisationSelect(
            attrs={
                'class': 'form-select',
            }
        )
    )


class OrganisationEditorRegistrationForm(EditorRegistrationForm, OrganisationEditorForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['localid'].help_text = f'A basic local ID is automatically generated using this organisation\'s short name. If there is another organisation sharing the same short name, a timestamp will be added to help ensure uniqueness.'
        self.fields['namespace'].widget = forms.HiddenInput()
        self.fields['short_name'].help_text = 'This will be used to automatically generate this registration\'s local ID suffix and will also be used as the namespace for future registrations associated with this organisation.'
        self.fields['organisation'].required = False


class IndividualEditorRegistrationForm(EditorRegistrationForm, IndividualEditorForm):
    pass


class ProjectEditorRegistrationForm(EditorRegistrationForm, ProjectEditorForm):
    pass


class PlatformEditorRegistrationForm(EditorRegistrationForm, PlatformEditorForm):
    pass


class OperationEditorRegistrationForm(EditorRegistrationForm, OperationEditorForm):
    pass


class InstrumentEditorRegistrationForm(EditorRegistrationForm, InstrumentEditorForm):
    pass


class AcquisitionCapabilitiesEditorRegistrationForm(EditorRegistrationForm, AcquisitionCapabilitiesEditorForm):
    pass


class AcquisitionEditorRegistrationForm(EditorRegistrationForm, AcquisitionEditorForm):
    pass


class ComputationCapabilitiesEditorRegistrationForm(EditorRegistrationForm, ComputationCapabilitiesEditorForm):
    pass


class ComputationEditorRegistrationForm(EditorRegistrationForm, ComputationEditorForm):
    pass


class ProcessEditorRegistrationForm(EditorRegistrationForm, ProcessEditorForm):
    pass


class DataCollectionEditorRegistrationForm(EditorRegistrationForm, DataCollectionEditorForm):
    pass


class CatalogueEditorRegistrationForm(EditorRegistrationForm, CatalogueEditorForm):
    pass


class StaticDatasetEntryEditorRegistrationForm(EditorRegistrationForm, StaticDatasetEntryEditorForm):
    pass


class DataSubsetEditorRegistrationForm(EditorRegistrationForm, DataSubsetForm):
    pass


class WorkflowEditorRegistrationForm(EditorRegistrationForm, WorkflowEditorForm, WorkflowOpenAPISpecificationForm):
    pass