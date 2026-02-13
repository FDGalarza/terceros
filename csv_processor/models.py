from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    contador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clientes')

    def __str__(self):
        return self.nombre
    
class Tarea(models.Model):
    ESTADO_CHOICES = [
        ('pendiente'  , 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada' , 'Completada'),
    ]

    titulo            = models.CharField(max_length=255)
    descripcion       = models.TextField(blank=True, null=True)
    fecha             = models.DateField()
    fecha_vencimiento = models.DateField(null=True, blank=True)  # Nuevo campo de fecha de vencimiento
    estado            = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    usuario           = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_completado  = models.DateTimeField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='tareas', null=True, blank=True)

    def __str__(self):
        return self.titulo
    
class Profile(models.Model):
    user     = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    profesion = models.CharField(max_length=100, blank=True, null=True)
    areaOperativa = models.CharField(max_length=100, blank=True, null=True)
    nombreLogo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
    

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class ControlActualizacionMensual(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ultima_actualizacion = models.DateField()

    def __str__(self):
        return f"{self.usuario.username} - {self.ultima_actualizacion}"



class Concepto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    contador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conceptos')

    def __str__(self):
        return self.nombre

class CuentaCobro(models.Model):
    ESTADO_CUENTA_CHOICES = [
        ('creada', 'Creada'),
        ('enviada', 'Enviada'),
        ('pagada', 'Pagada'),
    ]

    MESES_CHOICES = [
        ('1', 'Enero'),
        ('2', 'Febrero'),
        ('3', 'Marzo'),
        ('4', 'Abril'),
        ('5', 'Mayo'),
        ('6', 'Junio'),
        ('7', 'Julio'),
        ('8', 'Agosto'),
        ('9', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre'),
    ]

    tarea = models.OneToOneField(Tarea, on_delete=models.CASCADE, related_name='cuenta_cobro', null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cuentas_cobro')
    estado = models.CharField(max_length=20, choices=ESTADO_CUENTA_CHOICES, default='creada')
    fecha_creacion = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    
    # Nuevos campos
    concepto = models.ForeignKey(Concepto, on_delete=models.SET_NULL, null=True, blank=True, related_name='cuentas_cobro')
    valor = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True)
    mes = models.CharField(max_length=2, choices=MESES_CHOICES, null=True, blank=True)
    anio = models.IntegerField(null=True, blank=True, default=timezone.now().year)



    def __str__(self):
        return f"Cuenta de Cobro - {self.tarea.titulo} ({self.cliente.nombre})"

@receiver(post_save, sender=Tarea)
def actualizar_cuenta_cobro(sender, instance, **kwargs):
    """
    Automates the update of CuentaCobro when Tarea is completed.
    """
    if instance.estado == 'completada':
        try:
            cuenta = instance.cuenta_cobro
            from django.utils import timezone
            from datetime import timedelta
            
            # Solo actualizar si no tiene fechas asignadas previamente
            if not cuenta.fecha_creacion:
                cuenta.fecha_creacion = timezone.now().date()
                cuenta.fecha_vencimiento = cuenta.fecha_creacion + timedelta(days=15)
                cuenta.save()
        except CuentaCobro.DoesNotExist:
            pass  # No todas las tareas tienen cuenta de cobro

class Comentario(models.Model):
    cuenta = models.ForeignKey(CuentaCobro, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario en {self.cuenta} - {self.fecha_creacion}"

