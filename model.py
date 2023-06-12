import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

def recomendacion(titulo):
    # Leer el conjunto de datos
    df = pd.read_csv(r'movies_dataset_ml.csv')
    
    # Seleccionar las características a utilizar
    caracteristicas = ['budget', 'revenue', 'vote_average', 'popularity']
    X = df[caracteristicas]
    
    # Normalizar las características
    scaler = MinMaxScaler()
    X_norm = scaler.fit_transform(X)
    
    # Obtener el índice de la película ingresada
    idx = df[df['title'] == titulo].index[0]
    
    # Calcular la similitud del coseno con el resto de las películas
    similitudes = cosine_similarity(X_norm[idx].reshape(1, -1), X_norm)[0]
    
    # Ordenar las películas por similitud y seleccionar las 5 más similares
    indices_similares = similitudes.argsort()[::-1][1:6]
    peliculas_similares = df.iloc[indices_similares]['title'].tolist()
    
    return peliculas_similares