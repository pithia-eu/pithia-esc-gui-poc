from django import forms


class InstitutionForLoginSessionForm(forms.Form):
    def __init__(self, institution_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institutions'].choices = institution_choices

    institutions = forms.ChoiceField(
        choices=(),
        required=True,
        label='Select an Institution',
        widget=forms.Select(attrs={
            'class': 'form-select mb-3',
        })
    )

    next = forms.URLField(widget=forms.HiddenInput())