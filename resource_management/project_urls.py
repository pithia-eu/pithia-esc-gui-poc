from django.urls import path

from . import views

urlpatterns = [
    path('<project_id>/delete/', views.delete_project, name='delete_project'),
    path('<project_id>/update/', views.update_project, name='update_project'),
]
