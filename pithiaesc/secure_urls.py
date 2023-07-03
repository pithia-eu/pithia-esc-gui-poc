from django.urls import include, path

from . import views
from browse.views import schemas
from user_management import views as user_management_views

urlpatterns = [
    path('dashboard/', views.index_admin, name='data_provider_home'),
    path('logout/', views.logout, name='logout'),
    path('', include('update.urls')),
    path('', include('delete.urls')),
    path('', include('utils.urls')),
    path('manage/', include('resource_management.urls')),
    path('register/', include('register.urls')),
    path('schemas/', schemas, name='schemas'),
    path('validate/', include('validation.urls')),
    path('institutions/', user_management_views.join_perun_organisation, name='join_perun_organisation'),
    path('institutions/<institution_id>/', user_management_views.join_perun_organisation_subgroup, name='join_perun_organisation_subgroup'),
]
