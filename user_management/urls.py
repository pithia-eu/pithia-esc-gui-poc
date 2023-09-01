from django.urls import path
from . import views

urlpatterns = [
    path('update-perun-organisation-list/', views.update_perun_organisation_list, name='update_perun_organisation_list'),
    # path('perun-set-login/', views.save_perun_info, name='save_perun_info'),
    path('perun-login/', views.perun_login, name='perun_login'),
    
    # Perun login test
    path('perun-login-test/', views.perun_login_test, name='perun_login_test'),
]
