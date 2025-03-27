from setuptools import setup, find_packages

setup(
    name='procesar_csv',  # El nombre de tu aplicación
    version='0.1',
    packages=find_packages(),
    include_package_data=True,  # Para incluir archivos estáticos y plantillas
    install_requires=[
        'django>=3.0,<5.0',  # Django y otras dependencias que puedas necesitar
        'asgiref==3.8.1',
        'Django==5.1.7',
        'et_xmlfile==2.0.0',
        'numpy==2.2.4',
        'openpyxl==3.1.5',
        'pandas==2.2.3',
        'python-dateutil==2.9.0.post0',
        'pytz==2025.2',
        'six==1.17.0',
        'sqlparse==0.5.3',
        'tzdata==2025.2',
    ],
    entry_points={
        'console_scripts': [
            'procesar_csv=procesar_csv.manage:main',  # Comando que ejecuta manage.py
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',  # Actualiza esto según tu licencia
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # O cualquier versión de Python que uses
)
