from django.urls import path

from . import views

urlpatterns = [
    path('<instrument_id>/delete/', views.delete_instrument, name='delete_instrument'),
    path('<instrument_id>/update/', views.update_instrument, name='update_instrument'),
]
