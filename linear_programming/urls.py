from django.urls import path, include
from . import views

urlpatterns = [
   # Método Gráfico (página principal)
    path('', views.graphical_method_view, name='graphical_method'),
    
    # Placeholders para futuros métodos
    path('simplex/', views.simplex_method_placeholder, name='simplex_placeholder'),
    # ¡IMPORTANTE! Asegúrate de que el 'name' coincida EXACTAMENTE con lo que usas en el {% url %}
    path('dos-fases/', views.two_phase_method_placeholder, name='two_phase_method_placeholder'), 
]
