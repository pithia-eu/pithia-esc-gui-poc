from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select the metadata files you would like to upload:', widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
