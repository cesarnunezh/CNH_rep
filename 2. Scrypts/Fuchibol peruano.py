"""
@author: César Núñez
"""
# Importamos las librerías que utilizaremos
import pandas as pd
import numpy as np
import requests
import os

# Seteamos el directorio de trabajo
os.chdir('D:/1. Documentos/0. Bases de datos/9. Futbol')

# Creando la base de datos de jugadores. Como solo hay información desde el 2015, generamos un loop

for anio in range(2015, 2023):

    if anio == 2015:
        url = 'https://fbref.com/en/comps/44/' + str(anio) + '/stats/' + str(anio) + '-Liga-1-Stats'
        response = requests.get(url).text.replace('<!--', '').replace('-->', '')
        df_jugadores = pd.read_html(response, header=1)[2]
        df_jugadores["year"] = anio
    else:
        url = 'https://fbref.com/en/comps/44/' + str(anio) + '/stats/' + str(anio) + '-Liga-1-Stats'
        response = requests.get(url).text.replace('<!--', '').replace('-->', '')
        df_alterna = pd.read_html(response, header=1)[2]
        df_alterna["year"] = anio
        df_jugadores = pd.concat([df_jugadores , df_alterna])

# Eliminamos las filas que repiten los nombres de las variables
df_jugadores = df_jugadores.loc[df_jugadores["Rk"] != 'Rk']

# Guardamos la base de datos.
df_jugadores.to_csv('jugadores_liga1.csv', index=False)

# Creando la base de datos de partidos.

for anio in range(2014, 2023) :

    if anio == 2014 :
        url= 'https://fbref.com/en/comps/44/' + str(anio) + '/schedule/' + str(anio) + '-Liga-1-Scores-and-Fixtures#sched_all'
        df_partidos = pd.read_html(response, header=0)[0]
    else :
        url= 'https://fbref.com/en/comps/44/' + str(anio) + '/schedule/' + str(anio) + '-Liga-1-Scores-and-Fixtures#sched_all'
        response = requests.get(url).text.replace('<!--', '').replace('-->', '')
        df_alterna = pd.read_html(response, header=0)[0]
        df_partidos = pd.concat([df_partidos , df_alterna])

# Eliminamos las filas que repiten los nombres de las variables y las NaN
df_partidos = df_partidos.dropna(how='all')

# Guardamos la base de datos.
df_partidos.to_csv('partidos_liga1.csv', index=False)