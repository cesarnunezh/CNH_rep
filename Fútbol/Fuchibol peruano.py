"""
@project: Datos del fútbol peruano
@author: César Núñez
"""
################################################################################################
###############################IMPORTANDO LA DATA###############################################
################################################################################################

# Importamos las librerías que utilizaremos
import pandas as pd
import numpy as np
import requests
import os
import time

# Seteamos el directorio de trabajo
os.chdir('D:/1. Documentos/0. Bases de datos/9. Futbol')

directorio = {'Libertadores'    : 'https://fbref.com/en/comps/14/2022/stats/2022-Copa-Libertadores-Stats',
              'Liga 1 Perú'     : 'https://fbref.com/en/comps/44/2022/stats/2022-Liga-1-Stats',
              'Sudamericana'    : 'https://fbref.com/en/comps/205/2022/stats/2022-Copa-Sudamericana-Stats',
              'Argentina'       : 'https://fbref.com/en/comps/21/2019-2020/stats/2019-2020-Primera-Division-Stats',
              'Bolivia'         : 'https://fbref.com/en/comps/74/2022/stats/2022-Primera-Division-Stats',
              'Brasil - Serie A': 'https://fbref.com/en/comps/24/2022/stats/2022-Serie-A-Stats',
              'Brasil - Serie B': 'https://fbref.com/en/comps/38/2020/stats/2020-Serie-B-Stats',
              'Chile'           : 'https://fbref.com/en/comps/35/2022/stats/2022-Primera-Division-Stats',
              'Colombia'        : 'https://fbref.com/en/comps/41/2022/stats/2022-Primera-A-Stats',
              'Ecuador'         : 'https://fbref.com/en/comps/58/2022/stats/2022-Serie-A-Stats',
              'Mexico'          : 'https://fbref.com/en/comps/31/2021-2022/stats/2021-2022-Liga-MX-Stats',
              'Paraguay'        : 'https://fbref.com/en/comps/61/2022/stats/2022-Primera-Division-Stats',
              'Uruguay'         : 'https://fbref.com/en/comps/45/2021/stats/2021-Primera-Division-Stats',
              'Venezuela'       : 'https://fbref.com/en/comps/105/2022/stats/2022-Liga-FUTVE-Stats',
              'España - 2da'    : 'https://fbref.com/en/comps/17/2021-2022/stats/2021-2022-Segunda-Division-Stats'}

ligas = ['Libertadores', 'Perú' , 'Sudamericana', 'Argentina' , 'Bolivia' , 'Brasil-A' , 'Brasil-B', 'Chile' , 'Colombia',
         'Ecuador', 'Mexico', 'Paraguay' , 'Uruguay' , 'Venezuela' , 'España-B']
links = ['-Copa-Libertadores-Stats' , '-Liga-1-Stats' , '-Copa-Sudamericana-Stats', '-Primera-Division-Stats', '-Primera-Division-Stats' ,
         '-Serie-A-Stats', '-Serie-B-Stats' , '-Primera-Division-Stats', '-Primera-A-Stats', '-Serie-A-Stats', '-Liga-MX-Stats',
         '-Primera-Division-Stats', '-Primera-Division-Stats', '-Liga-FUTVE-Stats', '-Segunda-Division-Stats']
number = ['14', '44', '205', '21', '74', '24', '38', '35', '41', '58', '31', '61', '45', '105', '28']


# Creando la base de datos de jugadores. Como solo hay información desde el 2015, generamos un loop
contador_0 = 0
for anio in range(2015, 2023):
    contador = 0
    for link in links:
        try:
            if anio == 2015 and (ligas[contador] != 'Mexico' and ligas[contador] != 'España-B') and contador_0 == 0:
                url = 'https://fbref.com/en/comps/' + number[contador] + '/' + str(anio) + '/stats/' + str(anio) + link
                response = requests.get(url).text.replace('<!--', '').replace('-->', '')
                df_jugadores = pd.read_html(response, header=1)[2]
                df_jugadores["year"] = anio
                df_jugadores["ligas"] = ligas[contador]
                time.sleep(10)
            elif anio == 2015 and (ligas[contador] != 'Mexico' and ligas[contador] != 'España-B') and contador_0 != 0:
                url = 'https://fbref.com/en/comps/' + number[contador] + '/' + str(anio) + '/stats/' + str(anio) + link
                response = requests.get(url).text.replace('<!--', '').replace('-->', '')
                df_alterna = pd.read_html(response, header=1)[2]
                df_alterna["year"] = anio
                df_alterna["ligas"] = ligas[contador]
                df_jugadores = pd.concat([df_jugadores , df_alterna])
                time.sleep(10)
            elif (ligas[contador] == 'Argentina' and anio <= 2020 and anio >=2017) or (ligas[contador] == 'Mexico') or (ligas[contador] == 'España-B'):
                url = 'https://fbref.com/en/comps/' + number[contador] + '/' + str(anio-1) + '-' + str(anio) + '/stats/' + str(anio-1) + '-' + str(anio) + link
                response = requests.get(url).text.replace('<!--', '').replace('-->', '')
                df_alterna = pd.read_html(response, header=1)[2]
                df_alterna["year"] = anio
                df_alterna["ligas"] = ligas[contador]
                df_jugadores = pd.concat([df_jugadores , df_alterna])
                time.sleep(5)
            else:
                url = 'https://fbref.com/en/comps/' + number[contador] + '/' + str(anio) + '/stats/' + str(anio) + link
                response = requests.get(url).text.replace('<!--', '').replace('-->', '')
                df_alterna = pd.read_html(response, header=1)[2]
                df_alterna["year"] = anio
                df_alterna["ligas"] = ligas[contador]
                df_jugadores = pd.concat([df_jugadores , df_alterna])
                time.sleep(5)

        except:
            print('error en' + str(anio) + ligas[contador])

        contador = contador + 1
    contador_0 = contador_0 +1


# Eliminamos las filas que repiten los nombres de las variables
df_jugadores = df_jugadores.loc[df_jugadores["Rk"] != 'Rk']

# Guardamos la base de datos.
df_jugadores.to_csv('jugadores_latam.csv', index=False)


links = ['-Copa-Libertadores-Scores-and-Fixtures' , '-Liga-1-Scores-and-Fixtures' , '-Copa-Sudamericana-Scores-and-Fixtures', '-Primera-Division-Scores-and-Fixtures', '-Primera-Division-Scores-and-Fixtures' ,
         '-Serie-A-Scores-and-Fixtures', '-Serie-B-Scores-and-Fixtures' , '-Primera-Division-Scores-and-Fixtures', '-Primera-A-Scores-and-Fixtures', '-Serie-A-Scores-and-Fixtures', '-Liga-MX-Scores-and-Fixtures',
         '-Primera-Division-Scores-and-Fixtures', '-Primera-Division-Scores-and-Fixtures', '-Liga-FUTVE-Scores-and-Fixtures', '-Segunda-Division-Scores-and-Fixtures']

# Creando la base de datos de partidos.
start_time = time.time()

contador_0 = 0
for anio in range(2015, 2023) :
    contador = 0
    for link in links:
        try:
            if anio == 2015 and (ligas[contador] != 'Mexico' and ligas[contador] != 'España-B') and contador_0 == 0:
                url= 'https://fbref.com/en/comps/' + number[contador] + '/' + str(anio) + '/schedule/' + str(anio) + link +'#sched_all'
                response = requests.get(url).text.replace('<!--', '').replace('-->', '')
                df_partidos = pd.read_html(response, header=0)[0]
                df_partidos['year'] = anio
                df_partidos['liga'] = ligas[contador]
                time.sleep(10)
            elif anio == 2015 and (ligas[contador] != 'Mexico' and ligas[contador] != 'España-B') and contador_0 != 0:
                url= 'https://fbref.com/en/comps/' + number[contador] + '/' + str(anio) + '/schedule/' + str(anio) + link +'#sched_all'
                response = requests.get(url).text.replace('<!--', '').replace('-->', '')
                df_alterna2 = pd.read_html(response, header=0)[0]
                df_alterna2['year'] = anio
                df_alterna2['liga'] = ligas[contador]
                df_partidos = pd.concat([df_partidos , df_alterna2])
                time.sleep(5)
            else :
                url= 'https://fbref.com/en/comps/' + number[contador] + '/' + str(anio) + '/schedule/' + str(anio) + link +'#sched_all'
                response = requests.get(url).text.replace('<!--', '').replace('-->', '')
                df_alterna2 = pd.read_html(response, header=0)[0]
                df_alterna2['year'] = anio
                df_alterna2['liga'] = ligas[contador]
                df_partidos = pd.concat([df_partidos , df_alterna2])
                time.sleep(5)
        except:
            print('error en' + str(anio) + ligas[contador])
        contador = contador +1
    contador_0 = contador_0 +1

elapsed_time = time.time() - start_time
print(f"Execution time: {elapsed_time} seconds")

# Eliminamos las filas que repiten los nombres de las variables y las NaN
df_partidos = df_partidos.dropna(how='all')

# Guardamos la base de datos.
df_partidos.to_csv('partidos_liga1.csv', index=False)

################################################################################################
###############################TRABAJANDO LA DATA###############################################
################################################################################################
'''

# Seteamos el directorio de trabajo
os.chdir('D:/1. Documentos/0. Bases de datos/9. Futbol')

df_partidos = pd.read_csv("partidos_liga1.csv")

df_partidos= df_partidos.rename(columns={'Round': 'Torneo', 'Wk': 'Fecha', 'Venue': 'Estadio', 'Referee': 'Arbitro'})

df_partidos = df_partidos.loc[ :,'Torneo':'Notes']

df_partidos = df_partidos.iloc[ 20: , :-2]

df_partidos['Date'] = pd.to_datetime(df_partidos['Date'])

df_partidos['anio'] = df_partidos['Date'].dt.year

df_partidos['Goles_local'] = pd.Series(dtype=int)
df_partidos['Goles_visita'] = pd.Series(dtype=int)
df_partidos['Resultado'] = pd.Series(dtype=str)

for i,rows in df_partidos.iterrows():
    goles = df_partidos.loc[i,'Score'].split('–')

    df_partidos.loc[i ,'Goles_local'] = goles[0]
    df_partidos.loc[i ,'Goles_visita'] = goles[1]

    if goles[0] > goles[1]:
        df_partidos.loc[i , 'Resultado'] = "L"
    elif goles[0] == goles[1]:
        df_partidos.loc[i , 'Resultado'] = "E"
    else:
        df_partidos.loc[i , 'Resultado'] = "V"

# Trabajando la base de datos de jugadores
os.chdir('D:/1. Documentos/0. Bases de datos/9. Futbol')
df_jugadores = pd.read_csv("jugadores_liga1.csv")
df_jugadores = df_jugadores.drop('Matches', axis=1)
df_jugadores = df_jugadores.drop('Rk', axis=1)

variables = ['Player', 'year']

df_jugadores['Unico'] = ~df_jugadores[variables].duplicated(keep=False)

duplicados = df_jugadores[df_jugadores.Unico == False]

duplicados = duplicados.groupby(['Player', 'year']).agg({'Nation': 'first', 'Pos': 'first', 'Squad' : '-'.join, 'Age': 'first',
                                               'Born':'first', 'MP': 'sum', 'Starts': 'sum', 'Min': 'sum', '90s': 'sum', 'Gls': 'sum',
                                               'Ast': 'sum', 'G+A': 'sum', 'G-PK': 'sum', 'PK': 'sum', 'PKatt': 'sum', 'CrdY': 'sum',
                                               'CrdR': 'sum'}).reset_index()

duplicados['Gls.1'] = pd.Series(dtype=float)
duplicados['Ast.1'] = pd.Series(dtype=float)
duplicados['G+A.1'] = pd.Series(dtype=float)
duplicados['G-PK.1'] = pd.Series(dtype=float)
duplicados['G+A-PK'] = pd.Series(dtype=float)

for i,rows in duplicados.iterrows():
    duplicados.loc[i ,'Gls.1'] = duplicados.loc[i ,'Gls'] / duplicados.loc[i ,'90s']
    duplicados.loc[i ,'Ast.1'] = duplicados.loc[i ,'Ast'] / duplicados.loc[i ,'90s']
    duplicados.loc[i ,'G+A.1'] = duplicados.loc[i ,'G+A'] / duplicados.loc[i ,'90s']
    duplicados.loc[i ,'G-PK.1'] = duplicados.loc[i ,'G-PK'] / duplicados.loc[i ,'90s']
    duplicados.loc[i ,'G+A-PK'] = (duplicados.loc[i ,'G+A'] - duplicados.loc[i ,'PK']) / duplicados.loc[i ,'90s']


unicos = df_jugadores[df_jugadores.Unico == True]
unicos = unicos.drop('Unico', axis =1)

df_jugadores = pd.concat([unicos, duplicados])
df_jugadores['id_jugador'] = pd.factorize(df_jugadores['Player'])[0] + 1

df_jugadores = df_jugadores.reset_index()
df_jugadores = df_jugadores.drop('index', axis = 1)

