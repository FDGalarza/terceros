from django import forms
<<<<<<< HEAD
from .models import Tarea
=======
>>>>>>> 9064dc4d67308753a97110cdc708e6e32e4e2a0d

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

<<<<<<< HEAD
#Formulario tareas
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'estado', 'fecha_vencimiento', 'fecha']  # Agregar fecha al formulario
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})  # Usar un widget de tipo 'date' para seleccionar fechas
        }

=======
>>>>>>> 9064dc4d67308753a97110cdc708e6e32e4e2a0d

