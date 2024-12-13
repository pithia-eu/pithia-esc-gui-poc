from django import forms

from metadata_editor.forms import (
    CatalogueDataSubsetForm,
    WorkflowEditorForm,
)


class CatalogueDataSubsetEditorUpdateForm(CatalogueDataSubsetForm):
    is_existing_datahub_file_used = forms.BooleanField(
        label='Continue using the same file for this source',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        initial=True
    )

    source_datahub_file_name = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
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