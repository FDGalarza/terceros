import os
import io
import pandas as pd
from django.shortcuts import render
from django.contrib import messages
from .forms import CSVUploadFrom
from openpyxl import Workbook
from django.http import HttpResponse

def procesar_csv(request):
    context = {}
    if request.method == "POST":
        form = CSVUploadFrom(request.POST, request.FILES)
        if form.is_valid():
            #obtener el formatod del archivo seleccionado
            file_format = form.cleaned_data['file_format']
            archivo     = request.FILES['csv_file']
            print(archivo.name)
            pd.set_option('display.max_rows', None)
            
            # Obtener el directorio donde está el archivo CSV que se sube
            csv_directory = os.path.dirname(archivo.name)  # obtiene el directorio del archivo CSV

            # Crear la ruta completa para el archivo de salida en el mismo directorio
            output_file_name = os.path.join(csv_directory, archivo.name)  # Usa el mismo nombre de archivo
            output_file_name = output_file_name.replace('csv', 'xlsx')  # Cambia la extensión de '.csv' a '.xlsx'

            try:
                
                # Intentar leer el archivo CSV con diferentes delimitadores
                try:
                    df = pd.read_csv(archivo, encoding='utf-8', delimiter=';')  # Si usa punto y coma como delimitador
                except UnicodeDecodeError:
                    try:
                        df = pd.read_csv(archivo, encoding='ISO-8859-1', delimiter=';')  # Si usa punto y  coma, con codificación ISO-8859-1
                    except UnicodeDecodeError:
                        df = pd.read_csv(archivo, encoding='Windows-1252', delimiter=';')  # Si usa punto y  coma, con codificación Windows-1252

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
                    
                    # hace merge de las columnas sumasdas con las demas columbas
                    df_grouped = pd.merge(df_grouped_I, df_grouped_J, on=['Tipo de Documento', 'Número identificación', 'DV',
                                                                          'Primer apellido del informado', 'Segundo apellido del informado',
                                                                          'Primer nombre del informado', 'Otros nombres del informado',
                                                                          'Razón social informado'], how='left') 
                    
                    # Crea el archivo Excel en memoria
                    output = io.BytesIO()

                     # Usa el motor 'openpyxl' para escribir el archivo Excel
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_grouped.to_excel(writer, index=False, sheet_name='Resumen')

                     # Prepara la respuesta HTTP para enviar el archivo como una descarga
                    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    response['Content-Disposition'] = 'attachment; filename="1007_san_m.xlsx"'

                     # Retorna la respuesta con el archivo Excel generado
                    return response


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
                    output = io.BytesIO()

                     # Usa el motor 'openpyxl' para escribir el archivo Excel
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_grouped.to_excel(writer, index=False, sheet_name='Resumen')

                     # Prepara la respuesta HTTP para enviar el archivo como una descarga
                    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    response['Content-Disposition'] = 'attachment; filename="1007_san_m.xlsx"'

                     # Retorna la respuesta con el archivo Excel generado
                    return response


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
                     output = io.BytesIO()

                     # Usa el motor 'openpyxl' para escribir el archivo Excel
                     with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_grouped.to_excel(writer, index=False, sheet_name='Resumen')

                     # Prepara la respuesta HTTP para enviar el archivo como una descarga
                     response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                     response['Content-Disposition'] = 'attachment; filename="1007_san_m.xlsx"'

                     # Retorna la respuesta con el archivo Excel generado
                     return response

                 

            except Exception as e:
                context['error'] = f"Ocurrio un error al procesar el archivo: {e}"

    else:
        form = CSVUploadFrom()

    
    context['form'] = form
    
    return render(request, 'csv_processor/procesar_csv.html', context)
