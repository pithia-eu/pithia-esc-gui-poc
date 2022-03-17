from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import UploadFileForm
from .metadata_helpers import handle_uploaded_metadata

# Create your views here.
class RegisterView(FormView):
    form_class = UploadFileForm
    template_name = 'register/index.html'
    success_url = '/register/'

    def post(self, request, *args, **kwargs):
        form_class = self.form_class
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        if form.is_valid():
            handle_uploaded_metadata(files)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register Models/Datasets'
        return context