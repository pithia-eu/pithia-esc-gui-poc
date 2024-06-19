from django.shortcuts import render

from metadata_editor.views import *


# Create your views here.

class ResourceUpdateWithEditorFormView(ResourceEditorFormView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class OrganisationUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    OrganisationEditorFormView):
    pass