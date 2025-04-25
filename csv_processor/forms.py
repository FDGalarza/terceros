from django import forms
from .models import Tarea
from django.contrib.auth.forms import AuthenticationForm

# Opciones de formato para el archivo CSV (estructuras diferentes)
FILE_CHOICES = [
    ('0', 'Seleccionar'),
    ('1005', 'Cargar Fomato 1005'),
    ('1006', 'Cargar Fomato 1006'),
    ('1007', 'Cargar Fomato 1007'),
]

EXCEL_CHOISES = [
    ('0', 'Seleccionar'),
    ('1', 'Proveedores'),
    ('2', 'Archivo 5007'),
]

class CSVUploadForm(forms.Form):
    #Campo para seleccionar el tipo de formato
    file_format = forms.ChoiceField(
        choices=FILE_CHOICES, label="Selecciona el Formato",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    #Campo para cargar el archvo CSV
    csv_file = forms.FileField(label="Archivo")

# form para proveedores
class ExcelUploadFrom(forms.Form):
    #Campo para seleccionar el tipo de formato
    excel_file_proveedor = forms.FileField(label="Proveedores")

#Formulario tareas
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'estado', 'fecha_vencimiento', 'fecha']  # Agregar fecha al formulario
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})  # Usar un widget de tipo 'date' para seleccionar fechas
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_vencimiento']



