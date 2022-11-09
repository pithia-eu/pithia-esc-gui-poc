from django import forms

INTERACTION_METHOD_CHOICES = [('api', 'API')]

class UploadUpdatedFileForm(forms.Form):
    files = forms.FileField(label='File Upload', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'class': 'form-control'
            }))

class UploadUpdatedDataCollectionFileForm(forms.Form):
    files = forms.FileField(label='File Upload', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'class': 'form-control',
            }))
    interaction_methods = forms.MultipleChoiceField(choices=INTERACTION_METHOD_CHOICES, required=False, widget=forms.CheckboxSelectMultiple(attrs={
                            'class': 'form-check-input'
                        }))
    api_specification_url = forms.CharField(label='Link to API Specification', required=False, widget=forms.TextInput(attrs={
                            'class': 'form-control'
                        }))
    api_specification_description = forms.CharField(label='Description', required=False, disabled=True, widget=forms.Textarea(attrs={
                            'class': 'form-control',
                            'rows': 3,
                            'style': 'resize: none;'
                        }))
