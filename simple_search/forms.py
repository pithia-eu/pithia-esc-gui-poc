from django import forms


class SimpleSearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a keyword...',
        })
    )

    exact = forms.BooleanField(
        label='Exact match',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )