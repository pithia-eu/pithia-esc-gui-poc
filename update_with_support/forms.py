from django import forms

from metadata_editor.forms import (
    CatalogueDataSubsetForm,
    WorkflowEditorForm,
)


class CatalogueDataSubsetEditorUpdateForm(CatalogueDataSubsetForm):
    def __init__(self, *args, data_collection_choices=..., catalogue_entry_choices=..., **kwargs):
        super().__init__(*args, data_collection_choices=data_collection_choices, catalogue_entry_choices=catalogue_entry_choices, **kwargs)
    
    is_existing_datahub_file_used = forms.BooleanField(
        label='Continue using the same file for this source',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        initial=True
    )


class WorkflowEditorUpdateForm(WorkflowEditorForm):
    workflow_details_file_source = forms.ChoiceField(
        label='Workflow Details Format',
        required=True,
        choices=(
            ('existing', 'Keep Using the Same File'),
            ('file_upload', 'Upload a New File'),
            ('external', 'Link to the Workflow Details File'),
        ),
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        })
    )