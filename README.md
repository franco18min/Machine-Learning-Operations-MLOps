![header](https://capsule-render.vercel.app/api?type=waving&height=190&section=header&text=%20Machine%20Learning%20Operations%20(MLOps)%20Project&fontSize=30&&color=957DAD&fontColor=ffffff&fontAlignY=35)

## Introduccion 
<p align="justify">

Mi proyecto de MLops enginner, donde trabajo en un dataset de peliculas en la que voy a realzar la transformacion de datos (ETL),Desarrollo de API consumiendo el dataset transformado para luego hacer deploy con render, con al analisis exploratorio de datos (EDA) para finalmente hacer las recomendaciones mediante machine learning

</p>

<div align="center">
 
</div>
 
## Tecnologia usada
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)
- seaborn 
- rake-nltk

## ETL

- Algunos campos, como belongs_to_collection, production_companies y otros están anidados, ¡deberán desanidarlos para poder y unirlos al dataset de nuevo hacer alguna de las consultas de la API! O bien buscar la manera de acceder a esos datos sin desanidarlos.

- Los valores nulos de los campos revenue, budget deben ser rellenados por el número 0.

- Los valores nulos del campo release date deben eliminarse.

- De haber fechas, deberán tener el formato AAAA-mm-dd, además deberán crear la columna release_year donde extraerán el año de la fecha de estreno.

- Crear la columna con el retorno de inversión, llamada return con los campos revenue y budget, dividiendo estas dos últimas revenue / budget, cuando no hay datos disponibles para calcularlo, deberá tomar el valor 0.

- Eliminar las columnas que no serán utilizadas, video,imdb_id,adult,original_title,poster_path y homepage

## Funciones API

Funciones usadas para mi API

- Se ingresa el mes en español y la funcion retorna la cantidad de peliculas que se estrenaron ese mes 

- Se ingresa el dia en español y la funcion retorna la cantidad de peliculas que se estrenaron ese dia

- Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.

- Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones.

- Se ingresa el nombre de un actor debiendo devolver el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno

- Se ingresa el nombre de un director debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.


## EDA

Se realizo una exploracion sobre los datos para encontrar observaciones y tambien anomalias en los datos


## Sistema de recomendacion

Este sistema de recomendación utiliza el contenido de los títulos de las películas para encontrar películas similares y hacer recomendaciones 
Aclaro que la api consume la funcion para realizar la prueba


## Deployment

 El deploy fue mediante render

## Link al video explicativo