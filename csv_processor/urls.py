from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('procesar_excel/', views.procesar_excel, name='procesar_excel'),
    path('proveedores/', views.proveedores, name='procesar_proveedores'),
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('kanban/', views.tablero_kanban, name='kanban'),
    path('actualizar_estado_tarea/', views.actualizar_estado_tarea, name='actualizar_estado_tarea'),
    path('enviar-tareas/', views.enviar_tareas),
    path('editar_tarea/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('procesar_csv/eliminar_tarea/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('tareas/historial/', views.historial_tareas_completadas, name='historial_tareas'),
    path('tareas/<int:tarea_id>/cambiar_estado/', views.cambiar_estado_tarea, name='cambiar_estado_tarea'),

    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('exportar_reporte_cliente/', views.exportar_reporte_cliente, name='exportar_reporte_cliente'),
    path('cuentas/', views.tablero_cuentas, name='tablero_cuentas'),
    path('cuentas/actualizar_estado/', views.actualizar_estado_cuenta, name='actualizar_estado_cuenta'),
    path('cuentas/reporte/', views.reporte_cuentas, name='reporte_cuentas'),
    
    # Nuevas URLs
    path('conceptos/', views.lista_conceptos, name='lista_conceptos'),
    path('conceptos/eliminar/<int:concepto_id>/', views.eliminar_concepto, name='eliminar_concepto'),
    path('cuentas/crear/', views.crear_cuenta_cobro, name='crear_cuenta_cobro'),
    path('cuentas/editar/<int:cuenta_id>/', views.editar_cuenta_cobro_modal, name='editar_cuenta_cobro_modal'),
    path('cuentas/generar/<int:cuenta_id>/', views.generar_documento_cuenta, name='generar_documento_cuenta'),
    path('cuentas/<int:cuenta_id>/comentarios/', views.listar_comentarios, name='listar_comentarios'),
    path('cuentas/<int:cuenta_id>/comentarios/agregar/', views.agregar_comentario, name='agregar_comentario'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)