from django import forms

class UploadFileForm(forms.Form):
    files = forms.FileField(label='Select the metadata files you would like to register:', widget=forms.ClearableFileInput(attrs={
                'multiple': True,
                'class': 'form-control'
            }))
