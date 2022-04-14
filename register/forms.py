from django import forms

class UploadFileForm(forms.Form):
    files = forms.FileField(label='Upload your metadata files (must be formatted in XML)', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'multiple': True,
                'class': 'form-control'
            }))
