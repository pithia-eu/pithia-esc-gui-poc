from django import forms

class GroupByForm(forms.Form):
    group_by = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=[
            ('', 'None'),
            ('namespace', 'Namespace'),
        ],
        initial=''
    )
