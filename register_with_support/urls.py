from django.urls import path

from . import views

urlpatterns = [
    path('organisation-wizard/', views.OrganisationRegisterWithoutFileFormView.as_view(), name='organisation_no_file'),
    path('individual-wizard/', views.IndividualRegisterWithoutFileFormView.as_view(), name='individual_no_file'),
]