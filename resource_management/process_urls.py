from django.urls import path

from . import views

urlpatterns = [
    path('<process_id>/delete/', views.delete_process, name='delete_process'),
    path('<process_id>/update/', views.update_process, name='update_process'),
]
