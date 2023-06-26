from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('', include('browse.urls')),
    path('ontology/', include('ontology.urls')),
    path('present/', include('present.urls')),
    path('search/', include('search.urls')),
    path('admin/', admin.site.urls),
    path('authorised/', include('pithiaesc.secure_urls')),
    path('update-perun-organisation-list/', views.update_perun_organisation_list, name='update_perun_organisation_list'),
    path('select-institution-subgroup/', views.select_institution_subgroup, name='select_institution_subgroup'),
    # path('perun-set-login/', views.save_perun_info, name='save_perun_info'),
    # path('perun-login/', views.perun_login, name='perun_login'),
    # perun_login_test
    # path('perun-login-test/', views.perun_login_test, name='perun_login_test'),
]
