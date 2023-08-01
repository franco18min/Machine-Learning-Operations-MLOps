#http://127.0.0.1:8000 

from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse
import json

#Se ingresa el mes en español y la funcion retorna la cantidad de peliculas que se estrenaron ese mes 
app= FastAPI(tittle = 'Proyecto MLOPS', description = 'proyecto Machine Learning Operations')
df = pd.read_csv(r'steam_games.csv')

@app.get("/genero")
async def genero(Año: int):
    # Aquí va tu código para obtener los 5 géneros más vendidos en el orden correspondiente
    df_filtered = df[df["release_year"].int.contains(Año)]
    top_genres = df_filtered["genre"].value_counts().head(5).index.tolist()
    return top_genres


#ML
#@app.get('/recomendacion/{titulo}')
#def recomendar_peliculas(titulo: str):
    #peliculas_similares = recomendacion(titulo)
    #return peliculas_similares