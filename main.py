#http://127.0.0.1:8000 

from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse
import json
from model import recomendacion

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

#Se ingresa el nombre de un actor debiendo devolver el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno
@app.get('/get_actor/{nombre_actor}')
async def get_actor(nombre_actor: str):
    actor_df = df[df['cast'].str.contains(nombre_actor)]
    total_return = actor_df['return'].sum()
    avg_return = actor_df['return'].mean()
    num_movies = len(actor_df)
    return f"El actor {nombre_actor} ha participado de {num_movies} cantidad de filmaciones, el mismo ha conseguido un retorno de {total_return} con un promedio de {avg_return} por filmación"

#Se ingresa el nombre de un director debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.
@app.get('/get_director/{nombre_director}')
async def get_director(nombre_director: str):
    director_df = df[df['director'] == nombre_director]
    total_return = director_df['return'].sum()
    movies = director_df[['title', 'release_date', 'return', 'budget', 'revenue']].to_dict('records')
    return {'director': nombre_director, 'total_return': total_return, 'movies': movies}

#ML
@app.get('/recomendacion/{titulo}')
def recomendar_peliculas(titulo: str):
    peliculas_similares = recomendacion(titulo)
    return peliculas_similares