#http://127.0.0.1:8000 

from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse
import json
#from model import recomendacion

#Se ingresa el mes en español y la funcion retorna la cantidad de peliculas que se estrenaron ese mes 
app= FastAPI(tittle = 'Proyecto MLOPS', description = 'proyecto Machine Learning Operations')
df = pd.read_csv(r'movies_dataset_final.csv')
@app.get('/peliculas_mes/{mes}')
async def cantidad_filmaciones_mes(mes: str):
    meses = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
             'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
    if mes.lower() not in meses:
        return {'error': 'Mes no válido'}
    mes_num = meses[mes.lower()]
    peliculas_mes = df[df['release_date'].str.contains(f'-{mes_num:02d}-', na=False)]
    cantidad = len(peliculas_mes)
    return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes.capitalize()}"

#Se ingresa el dia en español y la funcion retorna la cantidad de peliculas que se estrenaron ese dia
@app.get('/peliculas_dia/{dia}')
async def cantidad_filmaciones_dia(dia: str):
    dias = {'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3, 'viernes': 4, 'sábado': 5, 'domingo': 6}
    if dia.lower() not in dias:
        return {'error': 'Día no válido'}
    dia_num = dias[dia.lower()]
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    peliculas_dia = df[df['release_date'].dt.dayofweek == dia_num]
    cantidad = len(peliculas_dia)
    return f"{cantidad} cantidad de películas fueron estrenadas en los días {dia.capitalize()}"

#Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
@app.get('/score_titulo/{titulo}')
async def score_titulo(titulo: str):
    pelicula = df[df['title'].str.lower() == titulo.lower()]
    if pelicula.empty:
        return {'error': 'Película no encontrada'}
    titulo = pelicula.iloc[0]['title']
    anio = pelicula.iloc[0]['release_year']
    score = pelicula.iloc[0]['popularity']
    return f"La película {titulo} fue estrenada en el año {anio} con un score/popularidad de {score}"

#Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones.
@app.get('/votos_titulo/{titulo}')
async def votos_titulo(titulo: str):
    pelicula = df[df['title'].str.lower() == titulo.lower()]
    if pelicula.empty:
        return {'error': 'Película no encontrada'}
    if pelicula.iloc[0]['vote_count'] < 2000:
        return {'error': 'La película no cumple con la condición de tener al menos 2000 valoraciones'}
    titulo = pelicula.iloc[0]['title']
    anio = pelicula.iloc[0]['release_year']
    votos = pelicula.iloc[0]['vote_count']
    promedio = pelicula.iloc[0]['vote_average']
    return f"La película {titulo} fue estrenada en el año {anio}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio}"

#Ingresas la productora, retornando la ganancia total y la cantidad de peliculas que produjeron
@app.get('/productoras/{productora}')
def productoras(productora:str):
    # Filtrar el dataframe por la productora dada
    df_productora = df[df['production_companies'].apply(lambda x: productora in x)]
    # Calcular la cantidad de películas y la ganancia total
    cantidad = len(df_productora)
    ganancia_total = df_productora['revenue'].sum()
    return {'productora':productora, 'ganancia_total':ganancia_total, 'cantidad':cantidad}

#Ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo
@app.get('/retorno/{pelicula}')
def retorno(pelicula:str):
    # Filtrar el dataframe por el título dado
    df_pelicula = df[df['title'] == pelicula]
    # Extraer la inversión, la ganancia, el retorno y el año de lanzamiento
    inversion = df_pelicula['budget'].iloc[0]
    ganancia = df_pelicula['revenue'].iloc[0]
    retorno = df_pelicula['return'].iloc[0]
    año = int(df_pelicula['release_year'].iloc[0])
    response_data = {'pelicula':pelicula, 'inversion':inversion, 'ganancia':ganancia, 'retorno':retorno,'año':año}
    response_json = json.dumps(response_data)
    # Devolver los datos como una respuesta JSON
    return JSONResponse(content=response_json)

#ML
#@app.get('/recomendacion/{titulo}')
#def recomendacion_pelicula(titulo: str):
    #recomendaciones = recomendacion(titulo)
    #return {"recomendaciones": recomendaciones}