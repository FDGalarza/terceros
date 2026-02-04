from django import forms
from .models import Tarea, Concepto, CuentaCobro, Cliente
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


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class TareaForm(forms.ModelForm):
    generar_cuenta = forms.BooleanField(required=False, label="Genera cuenta de cobro")

    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'estado', 'fecha_vencimiento', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'})
        }





class ConceptoForm(forms.ModelForm):
    class Meta:
        model = Concepto
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CuentaCobroForm(forms.ModelForm):
    class Meta:
        model = CuentaCobro
        fields = ['cliente', 'concepto', 'valor', 'mes', 'anio']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'concepto': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'mes': forms.Select(attrs={'class': 'form-select'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CuentaCobroForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['cliente'].queryset = Cliente.objects.filter(contador=user)
            self.fields['concepto'].queryset = Concepto.objects.filter(contador=user)

