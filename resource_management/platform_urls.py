from django.urls import path

from . import views

urlpatterns = [
    path('<platform_id>/delete/', views.delete_platform, name='delete_platform'),
    path('<platform_id>/update/', views.update_platform, name='update_platform'),
]
