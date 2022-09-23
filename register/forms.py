from django import forms

EXECUTION_METHOD_CHOICES = [('api', 'API')]

class UploadFileForm(forms.Form):
    files = forms.FileField(label='File Upload', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'class': 'form-control',
                'multiple': True,
            }))

class UploadDataCollectionFileForm(forms.Form):
    files = forms.FileField(label='File Upload', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'class': 'form-control',
            }))
    execution_methods = forms.MultipleChoiceField(choices=EXECUTION_METHOD_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
                            'class': 'form-check-input'
                        }))
    api_specification_url = forms.CharField(label='Link to API Specification', required=False, disabled=True, widget=forms.TextInput(attrs={
                            'class': 'form-control'
                        }))
