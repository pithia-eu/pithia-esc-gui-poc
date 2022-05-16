from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label='XML metadata file input:', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'class': 'form-control'
            }))
