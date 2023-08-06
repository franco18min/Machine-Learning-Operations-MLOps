#http://127.0.0.1:8000 

#Importamos paquetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from model import prediction
from fastapi import FastAPI
import pandas as pd
import pandas as pd
import ast

#Titulo de mi deploy
app= FastAPI(tittle = 'Proyecto MLOPS', description = 'proyecto Machine Learning Operations')

#Cargamos el json que procesaremos para usarlo como Dataframe
rows = []
with open('steam_games.json') as f:
    for line in f.readlines():
        rows.append(ast.literal_eval(line))
df = pd.DataFrame(rows)

#FUNCIONES

#Se ingresa un año y devuelve una lista con los 5 géneros más lanzados en el orden correspondiente.
@app.get("/genres/{generos}")
def genres(year: str):   
    mask = df['release_date'].str.startswith(year, na=False)
    df_year = df[mask]
    top_genres = df_year['genres'].explode().value_counts().head(5).to_dict()
    return {"top_genres": top_genres}

#Se ingresa un año y devuelve una lista con los juegos lanzados en el año.
@app.get('/games/{juegos}')
def games(year: str):
    mask = df['release_date'].str.startswith(year, na=False)
    df_year = df[mask]
    games = df_year['title'].explode().value_counts().index.tolist()
    return {"games": games}

#Se ingresa un año y devuelve una lista con los 5 specs que más se repiten en el mismo en el orden correspondiente.
@app.get("/specs/{especificaciones}")
def specs(year: str):   
    mask = df['release_date'].str.startswith(year, na=False)
    df_year = df[mask]
    top_specs = df_year['specs'].explode().value_counts().head(5).to_dict()
    return {"top_specs": top_specs}

#Cantidad de juegos lanzados en un año con early access.
@app.get('/games_early_access/{juegos_acceso_anticipado}}')
def early_access(year: str):
    mask = (df['release_date'].str.startswith(year, na=False)) & (df['early_access'] == True)
    df_year = df[mask]
    games = len(df_year)
    return {"games": games}

#Según el año de lanzamiento, se devuelve una lista con la cantidad de registros que se encuentren categorizados con un análisis de sentimiento.
@app.get('/sentiment/{sentimiento}')
def sentiment(year: str):
    mask = df['release_date'].str.startswith(year, na=False)
    df_year = df[mask]
    sentiment = df_year['sentiment'].value_counts().to_dict()
    return {"sentiment": sentiment}

#Top 5 juegos según año con mayor metascore.
@app.get('/top_games/{top_juegos}')
def top_games(year: str):
    #df = pd.read_csv('steam_games.csv')
    mask = df['release_date'].str.startswith(year, na=False)
    df_year = df[mask]
    top_games = df_year.sort_values(by='metascore', ascending=False).head(5)[['title', 'metascore']].to_dict('records')
    return {"top_games": top_games}

#ML
@app.get('/prediction_price/{prediccion_precio}')
def prediction_price(release_year: int, earlyaccess: bool, metascore: float):
    return prediction(release_year, earlyaccess, metascore)