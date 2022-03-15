from django.forms import forms

class SearchForm(forms.Form):
    file = forms.FileField(label='Model or Dataset metadata file')

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'