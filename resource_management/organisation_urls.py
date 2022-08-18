from django.urls import path

from . import views

urlpatterns = [
    path('<organisation_id>/delete/', views.delete_organisation, name='delete_organisation'),
    path('<organisation_id>/update/', views.update_organisation, name='update_organisation'),
]
