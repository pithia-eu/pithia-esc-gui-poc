from django import forms


class RelatedMetadataForm(forms.Form):
    resource_id = forms.CharField(required=True)