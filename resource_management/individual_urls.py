from django.urls import path

from . import views

urlpatterns = [
    path('<individual_id>/delete/', views.delete_individual, name='delete_individual'),
    path('<individual_id>/update/', views.update_individual, name='update_individual'),
]
