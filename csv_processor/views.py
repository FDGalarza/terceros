from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import os
import io
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm , ExcelUploadFrom, TareaForm
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from django.http import HttpResponse
from datetime import date
from calendar import monthrange
from .models import Tarea, User


def obtener_usuario_predeterminado():
    return User.objects.get(username='Eliana')  # o el username que hayas creado

    # en tu vista:
    usuario = request.user if request.user.is_authenticated else obtener_usuario_predeterminado()


def procesar_csv(request):
    context = {}
    if request.method == "POST":
        form = CSVUploadForm (request.POST, request.FILES)
        if form.is_valid():
            #obtener el formatod del archivo seleccionado
            file_format = form.cleaned_data['file_format']
            archivo     = request.FILES['csv_file']

            # Validar que el archivo tenga la extensión '.csv'
            file_name, file_extension = os.path.splitext(archivo.name)

            if not validar_extension(file_extension, 0):
                context['form'] = form
                context['error'] = "Por favor, sube un archivo con extensión .csv"
                return render(request, 'csv_processor/procesar_csv.html', context)
            
            pd.set_option('display.max_rows', None)
            
            # Obtener el directorio donde está el archivo CSV que se sube
            csv_directory = os.path.dirname(archivo.name)  # obtiene el directorio del archivo CSV

            # Crear la ruta completa para el archivo de salida en el mismo directorio
            output_file_name = os.path.join(csv_directory, archivo.name)  # Usa el mismo nombre de archivo
            output_file_name = output_file_name.replace('csv', 'xlsx')  # Cambia la extensión de '.csv' a '.xlsx'

            try:
                
                # Intentar leer el archivo CSV con diferentes delimitadores
                df = leer_archivo(archivo, 0)

                #Evitar que ponga decimales
                df = df.apply(pd.to_numeric, errors='ignore').astype('Int64', errors='ignore')

                # Reemplaza las celdas vacías por texto vacío ('') en todo el DataFrame
                df = df.fillna(0)
                df = df.applymap(lambda x: '' if x == 0 else x)
                
                #procesar segun el formato seleccionado
                if file_format == '1006':

                    #convierte a numerico los valores de la columna impouestos doscontables
                    df[' Impuesto generado '] = pd.to_numeric(df[' Impuesto generado '], errors='coerce')
                    
                    df[' IVA recuperado en devoluciones en compras anuladas. rescindidas o resueltas '] = pd.to_numeric(df[' IVA recuperado en devoluciones en compras anuladas. rescindidas o resueltas '], errors='coerce')
                    
                    #agrupa y suma los valores de la columna I
                    df_grouped_I = df.groupby(['Tipo de Documento', 'Número identificación', 'DV',
                                               'Primer apellido del informado', 'Segundo apellido del informado',
                                               'Primer nombre del informado', 'Otros nombres del informado',
                                               'Razón social informado'])[' Impuesto generado '].sum().reset_index()
                    
                    #agrupa y suma los valores de la columna J
                    df_grouped_J = df.groupby(['Tipo de Documento', 'Número identificación', 'DV',
                                               'Primer apellido del informado', 'Segundo apellido del informado',
                                               'Primer nombre del informado', 'Otros nombres del informado',
                                               'Razón social informado'])[' IVA recuperado en devoluciones en compras anuladas. rescindidas o resueltas '].sum().reset_index()
                    
                    # Agrupa y suma los valores de la columna J
                    df_grouped_K = df.groupby(['Tipo de Documento', 'Número identificación', 'DV',
                                               'Primer apellido del informado', 'Segundo apellido del informado',
                                               'Primer nombre del informado', 'Otros nombres del informado',
                                               'Razón social informado'])['Impuesto al consumo'].sum().reset_index()

                    # Hace merge de las columnas sumadas con las demás columnas
                    merged_ij = pd.merge(df_grouped_I, df_grouped_J, on=[ 'Tipo de Documento', 'Número identificación', 'DV',
                                                                          'Primer apellido del informado', 'Segundo apellido del informado',
                                                                          'Primer nombre del informado', 'Otros nombres del informado',
                                                                          'Razón social informado'
                                                                        ], how='left')

                    df_grouped = pd.merge(merged_ij, df_grouped_K, on=[
                                                                        'Tipo de Documento', 'Número identificación', 'DV',
                                                                        'Primer apellido del informado', 'Segundo apellido del informado',
                                                                        'Primer nombre del informado', 'Otros nombres del informado',
                                                                        'Razón social informado'
                                                                      ], how='left')
                    
                    # Crea el archivo Excel en memoria
                    return crear_archivo_excel_respuesta(df_grouped, output_file_name, file_format)

                elif file_format == '1005':

                    #convierte a numerico los valores de la columna impouestos doscontables
                    df[' Impuesto descontable '] = pd.to_numeric(df[' Impuesto descontable '], errors='coerce')
                    
                    df[' IVA resultante por devoluciones en ventas anuladas, rescindidas o resueltas '] = pd.to_numeric(df[' IVA resultante por devoluciones en ventas anuladas, rescindidas o resueltas '], errors='coerce')
                    
                    #agrupa y suma los valores de la columna I
                    df_grouped_I = df.groupby(['Numero de identificación del informado', 'Tipo de Documento', 'DV', 
                                             'Primer apellido del informado', 'Segundo apellido del informado',
                                             'Razón social informado'])[' Impuesto descontable '].sum().reset_index()
                    
                    #agrupa y suma los valores de la columna J
                    df_grouped_J = df.groupby(['Numero de identificación del informado', 'Tipo de Documento', 'DV', 
                                             'Primer apellido del informado', 'Segundo apellido del informado',
                                             'Razón social informado'])[' IVA resultante por devoluciones en ventas anuladas, rescindidas o resueltas '].sum().reset_index()
                    
                    # hace merge de las columnas sumasdas con las demas columbas
                    df_grouped = pd.merge(df_grouped_I, df_grouped_J, on=['Numero de identificación del informado', 'Tipo de Documento', 'DV', 
                                                                          'Primer apellido del informado', 'Segundo apellido del informado',
                                                                          'Razón social informado'], how='left') 
                    
                    # Crea el archivo Excel en memoria
                    return crear_archivo_excel_respuesta(df_grouped, output_file_name, file_format)


                elif file_format == '1007':
                     
                     #convierte a numerico los valores de la columna impouestos doscontables
                     df[' Ingresos brutos recibidos  '] = pd.to_numeric(df[' Ingresos brutos recibidos  '], errors='coerce')
                    
                     df[' Devoluciones, rebajas y descuentos '] = pd.to_numeric(df[' Devoluciones, rebajas y descuentos '], errors='coerce')

                     #Agrupar por nit y sumar valores
                     #agrupa y suma los valores de la columna I
                     df_grouped_I = df.groupby(['Concepto', 'Tipo de documento', 'Número identificación del informado',
                                                'Primer apellido del informado', 'Segundo apellido del informado',
                                                'Primer nombre del informado', 'Otros nombres del informado',
                                                'Razón social informado', 'País de residencia o domicilio'])[' Ingresos brutos recibidos  '].sum().reset_index()
                    
                    #agrupa y suma los valores de la columna J
                     df_grouped_J = df.groupby(['Concepto', 'Tipo de documento', 'Número identificación del informado',
                                                'Primer apellido del informado', 'Segundo apellido del informado',
                                                'Primer nombre del informado', 'Otros nombres del informado',
                                                'Razón social informado', 'País de residencia o domicilio'])[' Devoluciones, rebajas y descuentos '].sum().reset_index()
                     
                     # hace merge de las columnas sumasdas con las demas columbas
                     df_grouped = pd.merge(df_grouped_I, df_grouped_J, on=['Concepto', 'Tipo de documento', 'Número identificación del informado',
                                                                           'Primer apellido del informado', 'Segundo apellido del informado',
                                                                           'Primer nombre del informado', 'Otros nombres del informado',
                                                                           'Razón social informado', 'País de residencia o domicilio'], how='left') 
                     
                     # Crea el archivo Excel en memoria
                     # Crea el archivo Excel en memoria
                     return crear_archivo_excel_respuesta(df_grouped, output_file_name, file_format)

                 

            except Exception as e:
                context['error'] = f"Ocurrio un error al procesar el archivo: {e}"

    else:
        form = CSVUploadForm ()

    
    context['form'] = form
    
    return render(request, 'csv_processor/procesar_csv.html', context)

def procesar_excel(request):
    context = {}
    
    if request.method == "POST":
        form = CSVUploadForm (request.POST, request.FILES)
        if form.is_valid():
            # Obtener el formato del archivo seleccionado
            file_format = form.cleaned_data['file_format']
            archivo = request.FILES['csv_file']  # 'csv_file' será el archivo subido por el usuario

            # Validar que el archivo tenga la extensión '.xlsx' para Excel
            file_name, file_extension = os.path.splitext(archivo.name)

            if not validar_extension(file_extension, 1):
                context['form'] = form
                context['error'] = "Por favor, sube un archivo con extensión .xlsx o .xls"
                return render(request, 'csv_processor/procesar_excel.html', context)
            

            if file_format == 0:
                context['form'] = form
                context['error'] = "Por favor, seleccione un formato"
                return render(request, 'csv_processor/procesar_excel.html', context)
            
            pd.set_option('display.max_rows', None)

            # Obtener el directorio donde está el archivo CSV que se sube
            csv_directory = os.path.dirname(archivo.name)  # obtiene el directorio del archivo CSV

             # Crear la ruta completa para el archivo de salida en el mismo directorio
            output_file_name = os.path.join(csv_directory, archivo.name)  # Usa el mismo nombre de archivo
            
            # Leer el archivo Excel
            try:
                # Se usa pd.read_excel para leer archivos Excel
                df = pd.read_excel(archivo, engine='openpyxl')  # Puedes especificar el 'engine' si es necesario
                
                # Evitar que ponga decimales
                df = df.apply(pd.to_numeric, errors='ignore').astype('Int64', errors='ignore')

                # Reemplaza las celdas vacías por texto vacío ('') en todo el DataFrame
                df = df.fillna(0)
                df = df.applymap(lambda x: '' if x == 0 else x)

                df.columns = df.columns.str.strip()
                print(df.columns)
                # Procesar según el formato seleccionado
                if file_format == '1006':
                    # Convierte a numérico los valores de la columna impuestos descontables
                    df['Impuesto generado'] = pd.to_numeric(df['Impuesto generado'], errors='coerce')
                    
                    df['IVA recuperado en devoluciones en compras anuladas. rescindidas o resueltas'] = pd.to_numeric(df['IVA recuperado en devoluciones en compras anuladas. rescindidas o resueltas'], errors='coerce')
                    
                    df['Impuesto al consumo'] = pd.to_numeric(df['Impuesto al consumo'], errors='coerce')
                    
                    # Agrupa y suma los valores de la columna I
                    df_grouped_I = df.groupby(['Tipo de Documento', 'Número identificación', 'DV',
                                               'Primer apellido del informado', 'Segundo apellido del informado',
                                               'Primer nombre del informado', 'Otros nombres del informado',
                                               'Razón social informado'])['Impuesto generado'].sum().reset_index()
                    
                    # Agrupa y suma los valores de la columna J
                    df_grouped_J = df.groupby(['Tipo de Documento', 'Número identificación', 'DV',
                                               'Primer apellido del informado', 'Segundo apellido del informado',
                                               'Primer nombre del informado', 'Otros nombres del informado',
                                               'Razón social informado'])['IVA recuperado en devoluciones en compras anuladas. rescindidas o resueltas'].sum().reset_index()
                    
                    # Agrupa y suma los valores de la columna J
                    df_grouped_K = df.groupby(['Tipo de Documento', 'Número identificación', 'DV',
                                               'Primer apellido del informado', 'Segundo apellido del informado',
                                               'Primer nombre del informado', 'Otros nombres del informado',
                                               'Razón social informado'])['Impuesto al consumo'].sum().reset_index()

                    # Hace merge de las columnas sumadas con las demás columnas
                    merged_ij = pd.merge(df_grouped_I, df_grouped_J, on=[ 'Tipo de Documento', 'Número identificación', 'DV',
                                                                          'Primer apellido del informado', 'Segundo apellido del informado',
                                                                          'Primer nombre del informado', 'Otros nombres del informado',
                                                                          'Razón social informado'
                                                                        ], how='left')

                    df_grouped = pd.merge(merged_ij, df_grouped_K, on=[
                                                                        'Tipo de Documento', 'Número identificación', 'DV',
                                                                        'Primer apellido del informado', 'Segundo apellido del informado',
                                                                        'Primer nombre del informado', 'Otros nombres del informado',
                                                                        'Razón social informado'
                                                                      ], how='left')
                    
                    # Crea el archivo Excel en memoria
                    return crear_archivo_excel_respuesta(df_grouped, output_file_name, file_format)

                elif file_format == '1005':
                    # Convierte a numérico los valores de la columna impuestos descontables
                    df['Impuesto descontable'] = pd.to_numeric(df['Impuesto descontable'], errors='coerce')
                    
                    df['IVA resultante por devoluciones en ventas anuladas, rescindidas o resueltas'] = pd.to_numeric(df['IVA resultante por devoluciones en ventas anuladas, rescindidas o resueltas'], errors='coerce')
                    
                    # Agrupa y suma los valores de la columna I
                    df_grouped_I = df.groupby(['Numero de identificación del informado', 'Tipo de Documento', 'DV', 
                                             'Primer apellido del informado', 'Segundo apellido del informado',
                                             'Razón social informado'])['Impuesto descontable'].sum().reset_index()
                    
                    # Agrupa y suma los valores de la columna J
                    df_grouped_J = df.groupby(['Numero de identificación del informado', 'Tipo de Documento', 'DV', 
                                             'Primer apellido del informado', 'Segundo apellido del informado',
                                             'Razón social informado'])['IVA resultante por devoluciones en ventas anuladas, rescindidas o resueltas'].sum().reset_index()
                    
                    # Hace merge de las columnas sumadas con las demás columnas
                    df_grouped = pd.merge(df_grouped_I, df_grouped_J, on=['Numero de identificación del informado', 'Tipo de Documento', 'DV', 
                                                                          'Primer apellido del informado', 'Segundo apellido del informado',
                                                                          'Razón social informado'], how='left') 
                    
                    # Crea el archivo Excel en memoria
                    return crear_archivo_excel_respuesta(df_grouped, output_file_name, file_format)

                elif file_format == '1007':
                    # Convierte a numérico los valores de la columna impuestos descontables
                    df['Ingresos brutos recibidos'] = pd.to_numeric(df['Ingresos brutos recibidos '], errors='coerce')
                    
                    df['Devoluciones, rebajas y descuentos'] = pd.to_numeric(df['Devoluciones, rebajas y descuentos'], errors='coerce')

                    # Agrupar por NIT y sumar valores
                    # Agrupa y suma los valores de la columna I
                    df_grouped_I = df.groupby(['Concepto', 'Tipo de documento', 'Número identificación del informado',
                                                'Primer apellido del informado', 'Segundo apellido del informado',
                                                'Primer nombre del informado', 'Otros nombres del informado',
                                                'Razón social informado', 'País de residencia o domicilio'])['Ingresos brutos recibidos'].sum().reset_index()
                    
                    # Agrupa y suma los valores de la columna J
                    df_grouped_J = df.groupby(['Concepto', 'Tipo de documento', 'Número identificación del informado',
                                                'Primer apellido del informado', 'Segundo apellido del informado',
                                                'Primer nombre del informado', 'Otros nombres del informado',
                                                'Razón social informado', 'País de residencia o domicilio'])['Devoluciones, rebajas y descuentos'].sum().reset_index()
                     
                     # Hace merge de las columnas sumadas con las demás columnas
                    df_grouped = pd.merge(df_grouped_I, df_grouped_J, on=['Concepto', 'Tipo de documento', 'Número identificación del informado',
                                                                           'Primer apellido del informado', 'Segundo apellido del informado',
                                                                           'Primer nombre del informado', 'Otros nombres del informado',
                                                                           'Razón social informado', 'País de residencia o domicilio'], how='left') 
                     
                     # Crea el archivo Excel en memoria
                    return crear_archivo_excel_respuesta(df_grouped, output_file_name, file_format)

            except Exception as e:
                context['error'] = f"Ocurrió un error al procesar el archivo: {e}"

    else:
        form = CSVUploadForm ()

    context['form'] = form
    
    return render(request, 'csv_processor/procesar_excel.html', context)

def proveedores(request):
    context = {}  # Definimos context al principio

    if request.method == 'POST':
        print(request)
        form = ExcelUploadFrom(request.POST, request.FILES)

        archivo = request.FILES.get('excel_file_proveedor')  # Obtenemos el archivo cargado
        if not archivo:
            context['form'] = form
            context['error'] = "Por favor, seleccione un archivo"
            return render(request, 'csv_processor/proveedores.html', context)

        # Intentar leer las hojas del archivo Excel
        try:
            df_1001 = pd.read_excel(archivo, sheet_name="1001")
            df_terceros = pd.read_excel(archivo, sheet_name="terceros proveedores")
        except ValueError:
            context['form'] = form
            context['error'] = "El archivo no contiene las hojas requeridas: '1001' y 'terceros_proveedores'."
            return render(request, 'csv_processor/proveedores.html', context)

        # Verificar si las columnas necesarias existen en ambas hojas
        if 'Número identificación del informado' not in df_1001.columns or 'nit_ter' not in df_terceros.columns:
            context['form'] = form
            context['error'] = "Las columnas 'Número identificación del informado' o 'nit_ter' no existen en el archivo"
            return render(request, 'csv_processor/proveedores.html', context)

        
        # Limpiar la columna 'nit_ter' quitando las comas y eliminando espacios antes de la validación
        df_terceros['nit_ter'] = df_terceros['nit_ter'].astype(str).str.replace(',', '', regex=False).str.strip()

        # Limpiar la columna 'Número identificación del informado' eliminando espacios
        df_1001['Número identificación del informado'] = df_1001['Número identificación del informado'].astype(str).str.strip()

        # Validación y marcado de proveedores
        proveedores_validos = df_1001['Número identificación del informado'].isin(df_terceros['nit_ter'])

        # Crear un archivo Excel con el resultado
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="resultado_proveedores.xlsx"'

        # Crear un workbook de openpyxl
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df_1001.to_excel(writer, sheet_name='1001', index=False)
            df_terceros.to_excel(writer, sheet_name='terceros_proveedores', index=False)
            
            # Acceder al archivo Excel ya creado
            workbook = writer.book
            worksheet_1001 = workbook['1001']

            # Establecer el color azul suave para los proveedores
            azul_suave = PatternFill(start_color="BCE0F5", end_color="BCE0F5", fill_type="solid")

            # Colorear las filas de los proveedores en azul suave
            for row in range(2, len(df_1001) + 2):  # Comenzamos en 2 para evitar la fila de cabeceras
                if proveedores_validos.iloc[row - 2]:  # Si la fila es un proveedor
                    for col in range(1, len(df_1001.columns) + 1):  # Recorremos todas las columnas
                        worksheet_1001.cell(row=row, column=col).fill = azul_suave

        return response

    else:
        # Si no es un POST, renderizamos el formulario vacío
        form = ExcelUploadFrom()
        context['form'] = form

    return render(request, 'csv_processor/proveedores.html', context)


#Funcion para validar la extensión del archivo
def validar_extension(extension, flag):
    if flag == 0:
        return extension.lower() == '.csv'
    elif flag == 1:
        return extension.lower() == '.xlsx'

#lee el archio
def leer_archivo(archivo, flagTipoArchivo):
    
    """Lee el archivo CSV y lo convierte en un DataFrame de pandas."""
    if flagTipoArchivo == 0:
        try:
            return pd.read_csv(archivo, encoding='utf-8', delimiter=';')
        except UnicodeDecodeError:
            try:
                return pd.read_csv(archivo, encoding='ISO-8859-1', delimiter=';')
            except UnicodeDecodeError:
                return pd.read_csv(archivo, encoding='Windows-1252', delimiter=';')
    elif flagTipoArchivo == 1:
         """Lee el archivo Excel y lo convierte en un DataFrame de pandas."""
         return pd.read_excel(archivo)
"""
Crea un archivo Excel en memoria a partir de un DataFrame y devuelve una respuesta HTTP 
que permite descargar el archivo Excel generado."""

def crear_archivo_excel_respuesta(df, output_file_name, file_sheet):
   
    """
    :param df: El DataFrame de pandas que contiene los datos a cdincluir en el archivo Excel.
    :param output_file_name: El nombre del archivo Excel que se enviará como descarga.
    :return: Respuesta HTTP con el archivo Excel generado.
    """
    # Crea el archivo Excel en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name= file_sheet)  # Escribe el DataFrame en la hoja 'Resumen'

    # Prepara la respuesta HTTP para enviar el archivo como una descarga
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{output_file_name}"'
    return response

#Vista para gestionar tareas
def tablero_kanban(request):
    try:
        hoy = date.today()
        primer_dia = hoy.replace(day=1)
        ultimo_dia = hoy.replace(day=monthrange(hoy.year, hoy.month)[1])

        if request.user.is_authenticated:
            usuario = request.user
        else:
            usuario = User.objects.get(username='Eliana')

        tareas_pendientes = Tarea.objects.filter(fecha__range=(primer_dia, ultimo_dia), estado='pendiente', usuario=usuario)
        tareas_en_progreso = Tarea.objects.filter(fecha__range=(primer_dia, ultimo_dia), estado='en_progreso', usuario=usuario)
        tareas_completadas = Tarea.objects.filter(fecha__range=(primer_dia, ultimo_dia), estado='completada', usuario=usuario)

        context = {
            'hoy': hoy,
            'tareas_por_estado': {
                'pendiente': tareas_pendientes,
                'en_progreso': tareas_en_progreso,
                'completada': tareas_completadas,
            },
        }
        return render(request, 'csv_processor/kanban.html', context)
    except Exception as e:
        import traceback
        print("⚠️ Error en vista kanban:", e)
        traceback.print_exc()
        return HttpResponse("Error interno del servidor", status=500)


def crear_tarea(request):
    if request.method == 'POST':

        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')

        if nombre and descripcion and fecha:
            try:
                # Si el usuario no está autenticado, usar un usuario por defecto
                if request.user.is_authenticated:
                    usuario = request.user
                else:
                    # Cambia "admin" por el nombre de tu usuario predeterminado
                    usuario = User.objects.get(username='Eliana')

                tarea = Tarea(
                    titulo=nombre,
                    descripcion=descripcion,
                    fecha=fecha,
                    usuario=usuario,
                )
                tarea.save()
                return redirect('kanban')

            except Exception as e:
                print("Error al guardar la tarea:", e)
        else:
            print("Datos incompletos")

    return render(request, 'csv_processor/crear_tarea.html')

@csrf_exempt
def actualizar_estado_tarea(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tarea_id = tarea_id = data.get('tarea_id') or data.get('id')
            nuevo_estado = data.get('estado')
            tarea = Tarea.objects.get(id=tarea_id)
            tarea.estado = nuevo_estado
            print(tarea.estado)
            tarea.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            print("Error al actualizar la tarea:", str(e))
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
