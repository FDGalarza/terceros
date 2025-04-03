from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('procesar_csv/', views.procesar_csv, name='procesar_csv'),
    path('procesar_excel/', views.procesar_excel, name='procesar_excel'),
    path('proveedores/', views.proveedores, name='procesar_proveedores'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)