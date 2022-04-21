from django import forms

class UploadFileForm(forms.Form):
    files = forms.FileField(label='XML metadata file input:', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'multiple': True,
                'class': 'form-control'
            }))
