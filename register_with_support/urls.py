from django.urls import path

from . import views

urlpatterns = [
    path('organisation-wizard/', views.OrganisationRegisterWithoutFileFormView.as_view(), name='organisation_no_file'),
    path('individual-wizard/', views.IndividualRegisterWithoutFileFormView.as_view(), name='individual_no_file'),
    path('project-wizard/', views.ProjectRegisterWithoutFileFormView.as_view(), name='project_no_file'),
    path('platform-wizard/', views.PlatformRegisterWithoutFormView.as_view(), name='platform_no_file'),
]