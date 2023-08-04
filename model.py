#Importamos librerias

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd

###################### Funcion para predecir el precio del juego y calcular RMSE ######################

def prediction(release_year: int, earlyaccess: bool, metascore: float):

    #Leemos el csv guardado
    df_limpio = pd.read_csv(r'steam_games.csv')

    # Selecciono las características y la variable objetivo
    X = df_limpio[['release_year', 'early_access', 'metascore']]
    y = df_limpio['price']

    # Elimino filas con valores faltantes en las características
    X = X.dropna()
    y = y[X.index]

    # Codifico variables categóricas
    X = pd.get_dummies(X)

    # Divido el conjunto de datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Entrenaminto del modelo
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluo el modelo
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)

    # Codificar las características
    features = pd.DataFrame({'release_year': [release_year], 'early_access': [earlyaccess], 'metascore': [metascore]})
    features = pd.get_dummies(features)
    
    # Asegurarse de que las características estén en el mismo orden que en el modelo entrenado
    features = features.reindex(columns=X.columns, fill_value=0)
    
    # Hacer la predicción
    price = model.predict(features)
    
    return {'price': price[0], 'rmse': rmse}