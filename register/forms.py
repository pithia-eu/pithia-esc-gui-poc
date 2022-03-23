from django import forms

class UploadFileForm(forms.Form):
    files = forms.FileField(label='Model and/or Data Collection XML metadata files', widget=forms.ClearableFileInput(attrs={
                'multiple': True,
                'class': 'form-control'
            }))
