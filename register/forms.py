from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label='File Input', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'class': 'form-control'
            }))
