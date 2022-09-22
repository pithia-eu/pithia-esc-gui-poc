from django import forms

EXECUTION_METHOD_CHOICES = [('none', 'None'),
                            ('url', 'URL (Specified within the XML Metadata File)'),
                            ('api', 'API')]

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
    execution_method = forms.ChoiceField(choices=EXECUTION_METHOD_CHOICES, widget=forms.RadioSelect(attrs={
                            'class': 'form-check-input'
                        }))
    api_specification_url = forms.CharField(label='Link to API Specification', required=False, disabled=True, widget=forms.TextInput(attrs={
                            'class': 'form-control'
                        }))
