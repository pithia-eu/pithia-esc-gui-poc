from django.urls import path

from . import views

urlpatterns = [
    path('organisations/<resource_id>/update-with-wizard/', views.OrganisationUpdateWithEditorFormView.as_view(), name='organisation_with_editor'),
]