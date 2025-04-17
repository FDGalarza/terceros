from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tarea(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
    ]

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    fecha_vencimiento = models.DateField(null=True, blank=True)  # Nuevo campo de fecha de vencimiento
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
    

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
=======

# Create your models here.
>>>>>>> 9064dc4d67308753a97110cdc708e6e32e4e2a0d
