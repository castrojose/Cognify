from django.urls import path
from . import views

urlpatterns = [
    path('', views.criminal_list, name='criminal_list'),
    path('simulate/<int:criminal_id>/', views.run_simulation, name='run_simulation'),
    path('impact-evaluation/', views.impact_evaluation, name='impact_evaluation'),
    path('add/', views.add_criminal, name='add_criminal'),  # Nueva ruta para agregar criminales
    path('rehabilitate-criminal/<int:criminal_id>/', views.rehabilitate_criminal_with_progress, name='rehabilitate_criminal_with_progress'),

]
