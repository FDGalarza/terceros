from django import forms

# Opciones de formato para el archivo CSV (estructuras diferentes)
FILE_CHOICES = [
    ('1005', 'Cargar Fomato 1005'),
    ('1006', 'Cargar Fomato 1006'),
    ('1007', 'Cargar Fomato 1007'),
]

class CSVUploadFrom(forms.Form):
    #Campo para seleccionar el tipo de formato
    file_format = forms.ChoiceField(choices=FILE_CHOICES, label="Selecciona el Formato")
    #Campo para cargar el archvo CSV
    csv_file = forms.FileField(label="")
