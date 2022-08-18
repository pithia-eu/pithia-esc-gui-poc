from django.urls import path

from . import views

urlpatterns = [
    path('<operation_id>/delete/', views.delete_operation, name='delete_operation'),
    path('<operation_id>/update/', views.update_operation, name='update_operation'),
]
