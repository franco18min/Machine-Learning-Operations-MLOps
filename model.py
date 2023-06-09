import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Leer el archivo CSV con las columnas seleccionadas y limpias
df_selected = pd.read_csv(r'movies_dataset_ml.csv')

# Manejo de valores nulos en la columna "title"
df_selected['title'] = df_selected['title'].fillna('')

# Crear el vectorizador TF-IDF y transformar los títulos de las películas
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df_selected['title'].astype('U'))

# Crear el modelo Nearest Neighbors y ajustarlo con la matriz TF-IDF
nn_model = NearestNeighbors(metric='cosine')
nn_model.fit(tfidf_matrix)

def recomendacion(title, num_recomendaciones=5):
    # Transformar el título de la película en una matriz TF-IDF
    title_tfidf = tfidf.transform([title])

    # Encontrar los índices y distancias de las películas más similares
    _, indices = nn_model.kneighbors(title_tfidf, n_neighbors=num_recomendaciones+1)

    # Obtener los índices de las películas (excluyendo la película de consulta)
    movie_indices = indices.flatten()[1:]

    # Obtener los títulos de las películas recomendadas
    recomendaciones = df_selected['title'].iloc[movie_indices].tolist()

    return recomendaciones