from django.urls import include, path

from . import views
from browse.views import schemas
from user_management import views as user_management_views

urlpatterns = [
    path('dashboard/', views.index, name='data_provider_home'),
    path('', include('update.urls')),
    path('', include('delete.urls')),
    path('', include('utils.urls')),
    path('manage/', include('resource_management.urls')),
    path('register/', include('register.urls')),
    path('schemas/', schemas, name='schemas'),
    path('validate/', include('validation.urls')),
    path('institutions/', user_management_views.list_joinable_perun_organisations, name='list_joinable_perun_organisations'),
    path('institutions/<institution_id>/', user_management_views.list_joinable_perun_organisation_subgroups, name='list_joinable_perun_organisation_subgroups'),
    path('choose-institution-for-session/', user_management_views.choose_perun_organisation_subgroup_for_session, name='choose_perun_organisation_subgroup_for_session'),
]
