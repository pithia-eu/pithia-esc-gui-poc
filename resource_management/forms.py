from django import forms

class UploadUpdatedFileForm(forms.Form):
    files = forms.FileField(label='File Upload', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'class': 'form-control'
            }))
