from django import forms

class GroupByForm(forms.Form):
    group_by = forms.ChoiceField(
        label='Group by',
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        choices=[
            ('', 'None'),
            ('namespace', 'Namespace'),
        ],
        initial=''
    )
