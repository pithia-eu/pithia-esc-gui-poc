from django.urls import path

from . import views

urlpatterns = [
    path('<computation_id>/delete/', views.delete_computation, name='delete_computation'),
    path('<computation_id>/update/', views.update_computation, name='update_computation'),
]
