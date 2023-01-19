from django import forms


class UploadUpdatedFileForm(forms.Form):
    files = forms.FileField(label='Select an XML file', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'class': 'form-control'
            }))

class UploadUpdatedDataCollectionFileForm(forms.Form):
    files = forms.FileField(label='Select an XML file', widget=forms.ClearableFileInput(attrs={
                'accept': 'application/xml',
                'class': 'form-control',
            }))

class UpdateDataCollectionInteractionMethodsForm(forms.Form):
    api_selected = forms.BooleanField(label='API', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))
    api_specification_url = forms.CharField(label='Link to API Specification', required=False, widget=forms.TextInput(attrs={
                            'class': 'form-control'
                        }))
    api_description = forms.CharField(label='Description', required=False, disabled=True, widget=forms.Textarea(attrs={
                            'class': 'form-control',
                            'rows': 3,
                            'style': 'resize: none;'
                        }))
