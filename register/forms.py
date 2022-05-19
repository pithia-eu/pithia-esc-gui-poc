from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a metadata file to upload:', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'class': 'form-control'
            }))
