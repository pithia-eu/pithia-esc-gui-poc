from django import forms

from metadata_editor.forms import WorkflowEditorForm


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