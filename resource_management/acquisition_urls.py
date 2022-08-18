from django.urls import path

from . import views

urlpatterns = [
    path('<acquisition_id>/delete/', views.delete_acquisition, name='delete_acquisition'),
    path('<acquisition_id>/update/', views.update_acquisition, name='update_acquisition'),
]
