import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'procesar_csv.settings')
django.setup()

def check_tables():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_name IN ('csv_processor_concepto', 'csv_processor_cuentacobro', 'csv_processor_comentario');
        """)
        rows = cursor.fetchall()
        print("Existing tables:", [row[0] for row in rows])

if __name__ == '__main__':
    check_tables()
