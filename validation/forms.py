from django import forms

class ApiSpecificationUrlValidationForm(forms.Form):
    api_specification_url = forms.URLField()