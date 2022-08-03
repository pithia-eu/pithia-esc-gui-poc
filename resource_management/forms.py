from django import forms

class UploadUpdatedFileForm(forms.Form):
    file = forms.FileField(label='File Upload', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'class': 'form-control'
            }))
