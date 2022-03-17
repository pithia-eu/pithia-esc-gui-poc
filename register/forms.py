from django import forms

class UploadFileForm(forms.Form):
    files = forms.FileField(label='Upload XML metadata files for Models/Data Collections', widget=forms.ClearableFileInput(attrs={
                'multiple': True,
                'class': 'form-control'
            }))
