from django.urls import path

from . import views

urlpatterns = [
    path('organisation-wizard/', views.OrganisationRegisterWithEditorFormView.as_view(), name='organisation_with_editor'),
    path('individual-wizard/', views.IndividualRegisterWithEditorFormView.as_view(), name='individual_with_editor'),
    path('project-wizard/', views.ProjectRegisterWithEditorFormView.as_view(), name='project_with_editor'),
]