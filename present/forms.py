from django import forms


class SwaggerViewModeForm(forms.Form):
    mode = forms.ChoiceField(
        label='View as',
        choices=(
            ('dev', 'Developer'),
            ('user', 'User'),
        ),
        widget=forms.Select(attrs={
            'class': 'form-select no-search'
        })
    )