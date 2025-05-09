from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

