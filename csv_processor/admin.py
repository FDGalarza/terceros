from django.contrib import admin
from .models import ControlActualizacionMensual, Tarea, Cliente
from .models import Profile

admin.site.register(Tarea)
admin.site.register(Profile)
admin.site.register(ControlActualizacionMensual)
admin.site.register(Cliente)
