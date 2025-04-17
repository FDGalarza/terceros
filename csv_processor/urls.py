from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('procesar_csv/', views.procesar_csv, name='procesar_csv'),
    path('procesar_excel/', views.procesar_excel, name='procesar_excel'),
    path('proveedores/', views.proveedores, name='procesar_proveedores'),
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('kanban/', views.tablero_kanban, name='kanban'),
    path('actualizar_estado_tarea/', views.actualizar_estado_tarea, name='actualizar_estado_tarea'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)