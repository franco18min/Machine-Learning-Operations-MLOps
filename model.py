import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv(r'movies_dataset_ml.csv')

def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''

    titulo = titulo.title()
    # Eliminar valores nulos en el DataFrame
    df.dropna(subset=['title'], inplace=True)

    # Crear vectorizador TF-IDF
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=5, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['title'])

    # Crear matriz de similitud dispersa
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix, dense_output=False)
    # Obtener índice de película correspondiente al título
    idx = df[df['title'] == titulo].index[0]
    
    # Obtener puntajes de similitud de película correspondiente al índice
    sim_scores = list(enumerate(cosine_sim[idx].toarray().ravel()))
    
    # Ordenar películas por puntaje de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Obtener índices de las 5 películas más similares
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    
    # Devolver lista de los 5 títulos de películas más similares
    return df['title'].iloc[movie_indices].tolist()