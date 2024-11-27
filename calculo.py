import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import os

archivo_datos = r'C:\Users\Usuario\OneDrive\Documentos\Univercidad\Pogramocion\calculo\modelo.txt'

# Verificar si el archivo existe y es accesible
if not os.path.isfile(archivo_datos):
    print(f"Error: No se encontró el archivo o la ruta no es válida: {archivo_datos}")
    exit()
try:
    datos_modelo = pd.read_csv(
        archivo_datos,
        sep=r'\s+',  
        skiprows=3 
    )
except Exception as error:
    print(f"Error al leer el archivo: {error}")
    exit()

# Corregir valores de HHMM
datos_modelo['HHMM'] = datos_modelo['HHMM'].astype(str).str.zfill(4)

# Crear columna de fecha combinando YYYYMMDD y HHMM
datos_modelo['MarcaTemporal'] = pd.to_datetime(
    datos_modelo['YYYYMMDD'].astype(str) + datos_modelo['HHMM'], 
    format='%Y%m%d%H%M', errors='coerce'  # Usar errors='coerce' para manejar valores inválidos
)

# Verificar si hay valores en la columna MarcaTemporal
fechas_invalidas = datos_modelo[datos_modelo['MarcaTemporal'].isna()]
if not fechas_invalidas.empty:
    print("Advertencia: Se encontraron valores de fecha/hora inválidos:")
    print(fechas_invalidas)
    datos_modelo.dropna(subset=['MarcaTemporal'], inplace=True)

# Configurar el índice como MarcaTemporal y eliminar columnas originales
datos_modelo.set_index('MarcaTemporal', inplace=True)
datos_modelo.drop(columns=['YYYYMMDD', 'HHMM'], inplace=True)

print("Datos cargados correctamente:")
print(datos_modelo.head())

# Matriz de dispersión para las primeras 1000 filas
scatter_matrix(
    datos_modelo.loc[datos_modelo.index[:1000], 'M(m/s)':'D(deg)'],
    alpha=0.2, figsize=(10, 10), diagonal='kde'
)
plt.show()

# Histograma de velocidades del viento
datos_modelo.loc[:, 'M(m/s)'].plot.hist(bins=np.arange(0, 35), edgecolor='black', alpha=0.7)
plt.title("Distribución de Velocidades del Viento (M(m/s))")
plt.xlabel("Velocidad (m/s)")
plt.ylabel("Frecuencia")
plt.show()

# Agregar columnas para 'year' y 'month'
datos_modelo['mes'] = datos_modelo.index.month
datos_modelo['año'] = datos_modelo.index.year

# Agrupar por año y mes y calcular la media
datos_mensuales = datos_modelo.groupby(by=['año', 'mes']).mean()
datos_mensuales['media_movil'] = datos_mensuales['M(m/s)'].rolling(5, center=True).mean()

# Visualizar tendencias
datos_mensuales[['M(m/s)', 'media_movil']].plot(figsize=(15, 6))
plt.title("Tendencias Mensuales de Velocidades del Viento")
plt.xlabel("Tiempo")
plt.ylabel("Velocidad del Viento (m/s)")
plt.show()
