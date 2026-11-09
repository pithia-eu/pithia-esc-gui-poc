from django import forms


class InstitutionForLoginSessionForm(forms.Form):
    def __init__(self, *args, institution_choices=[], **kwargs):
        super(InstitutionForLoginSessionForm, self).__init__(*args, **kwargs)
        self.fields['institutions'].choices = institution_choices
        self.label_suffix = ''

    institutions = forms.ChoiceField(
        choices=(),
        required=True,
        label='Available Institutions',
        widget=forms.Select(attrs={
            'class': 'form-select mb-3',
        })
    )

    next = forms.CharField(widget=forms.HiddenInput(), required=False)