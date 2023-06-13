#Username: RCastroPeraza
#Date: 2023 June 12

#Importing the libraries
from fastapi import FastAPI
import pandas as pd
import calendar 
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#import the data
data= pd.read_csv('datasets/DEset.csv')
df = pd.DataFrame(data)
df.drop_duplicates(subset='id',inplace=True)

credits=pd.read_csv('datasets/credits_filtered.csv')
df_credits=pd.DataFrame(credits)

ml_set=pd.read_csv('datasets/datos_con_repeticiones2.csv')
ml_data= pd.DataFrame(ml_set)
ml_data.drop_duplicates(subset='id',inplace=True)

#selected_features = ['genres_filtered','tagline','cast_filtered','crew_filtered','overview','production_companies_filtered']

#for feature in selected_features:
#  ml_data[feature] = ml_data[feature].fillna('')

#Create a FastAPI object
app=FastAPI()
#http://127.0.0.1:8000

#Bienvenida
@app.get("/")
def bienvenida():
    return "Esta API contiene 6 diferentes funciones para navegar a través de la información provista de películas"

#Films per month
df['release_date'] = pd.to_datetime(df['release_date']) 

@app.get("/cantidad_filmaciones_mes/{Mes}")
def cantidad_filmaciones_mes(Mes:str):
    '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes historicamente'''
    errormessage = 'Has ingresado un nombre de mes inválido, intenta otra vez ingresando el nombre del mes en español y sin ", gracias.'
    meses_validos = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    
    if Mes.lower() not in meses_validos:
        return errormessage

    No_mes = meses_validos.index(Mes.lower()) + 1
    
    df_mes = df[df['release_date'].dt.month == No_mes]
    No_peliculas = len(df_mes)

    return {'Mes':Mes, 'cantidad':No_peliculas}


#Films per day of the week
def convertir_dia(dia):
    dias_semana_espanol = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    dias_semana_ingles = list(calendar.day_name)

    dias_semana_espanol_es = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    dias_semana_ingles_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Crear un diccionario de mapeo
    mapeo_dias = dict(zip(dias_semana_espanol_es, dias_semana_ingles_en))

    if dia in dias_semana_espanol:
        # Obtener el índice del día en español
        indice = dias_semana_espanol.index(dia)

        # Obtener el equivalente en inglés
        dia_ingles = dias_semana_ingles[indice]

        return dia_ingles
    elif dia in dias_semana_ingles:
        return dia

    return None

@app.get("/cantidad_filmaciones_dia/{Dia}")
def cantidad_filmaciones_dia(Dia:str):
    '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrebaron ese dia historicamente'''
    errormessage = 'Has ingresado un nombre de día inválido, intenta otra vez'
    dias_validos = ['lunes', 'martes', 'miércoles', 'jueves','viernes','sábado', 'domingo']
    
    if Dia.lower() not in dias_validos:
        return errormessage
    
    day=convertir_dia(Dia.lower())
    
    df_dia = df[df['release_date'].dt.strftime("%A") == day]
    No_peliculas = len(df_dia)

    return {'dia':Dia, 'cantidad':No_peliculas}


#Films by title 

@app.get("/score_titulo/{titulo}")
def score_titulo(titulo:str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score'''
    df_titulo = df[df['title'] == titulo]
    df_titulo.drop(['Unnamed: 0', 'budget', 'id', 'original_language', 'overview',
        'release_date', 'revenue', 'runtime', 'status', 'tagline',
        'vote_average', 'vote_count', 'genres_filtered',
       'spoken_languages_filtered', 'production_companies_filtered',
       'production_countries_filtered', 'belongs_to_collection_filtered',
        'return'], axis=1,inplace=True)

    year= int(df_titulo['release_year'])
    popularity=float(df_titulo['popularity'])

    return  {'titulo':titulo, 'anio':year, 'popularidad':popularity}
#Films by title and the votes

@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo:str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. 
    La misma variable deberá de contar con al menos 2000 valoraciones, 
    caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.'''
    df_titulo = df[df['title'] == titulo]
    df_titulo.drop(['Unnamed: 0', 'budget', 'id', 'original_language', 'overview',
        'release_date', 'revenue', 'runtime', 'status', 'tagline',
        'popularity', 'genres_filtered', 'spoken_languages_filtered', 
        'production_companies_filtered', 'production_countries_filtered', 
        'belongs_to_collection_filtered','return'], axis=1,inplace=True)

    year= int(df_titulo['release_year'])
    vote_count= int(df_titulo['vote_count'])
    vote_average=float(df_titulo['vote_average'])

    if vote_count >= 2000:
        return {'titulo': titulo, 'anio': year, 'voto_total': vote_count, 'voto_promedio': vote_average}
    else:
        return f"{titulo} no contó con un mínimo de 2000 valoraciones"

    
    
#Films by the cast

def get_ids_cast(name):
    ids = []
    for cast_list in df_credits['cast_filtered']:
        if name in cast_list:
            ids.append(df_credits.loc[df_credits['cast_filtered'] == cast_list, 'id'].to_list())

    result = [num for sublist in ids for num in sublist]

    return result

@app.get("/get_actor/{name}")
def get_actor(name:str):
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, la cantidad de películas que en las que ha participado y el promedio de retorno'''
    total_return=0
    ids_films= get_ids_cast(name)

    for id in ids_films:
        if id in df['id'].values:
            total_return += float(df.loc[df['id'] == id, 'return'])
    
    total_films=len(ids_films)
    average_return=total_return/total_films

    return {'actor':name, 'cantidad_filmaciones':total_films, 'retorno_total':total_return, 'retorno_promedio':average_return}

#Films by the director

df_credits.fillna('No Director Info',inplace=True)

def get_ids_crew(name):
    ids = []
    for i in range(df_credits.shape[0]):
        if name == df_credits['crew_filtered'].iloc[i]:
            ids.append(df_credits['id'].iloc[i])

    return ids

@app.get("/get_director/{name}")
def get_director(name:str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.'''
    ids_films = get_ids_crew(name)

    dataset_per_director = df.query('id in @ids_films').copy()

    dataset_per_director['Títulos'] = dataset_per_director['title'].astype(str)
    dataset_per_director['Fecha_de_Lanzamiento'] = dataset_per_director['release_date'].astype(str)
    dataset_per_director['Retorno'] = dataset_per_director['return'].astype(float)
    dataset_per_director['Presupuesto'] = dataset_per_director['budget'].astype(float)
    dataset_per_director['Recaudación'] = dataset_per_director['revenue'].astype(float)
    dataset_per_director['Ganancia'] = dataset_per_director['revenue'].astype(float) - dataset_per_director['budget'].astype(float)

    columns_to_keep = ['Títulos', 'Fecha_de_Lanzamiento', 'Retorno', 'Presupuesto', 'Recaudación', 'Ganancia']
    dataset_per_director = dataset_per_director[columns_to_keep]

    total_return = dataset_per_director['Retorno'].sum()
    rows=dataset_per_director.shape[0]

    return {'director':name, 'retorno_total_director':total_return, 
    'peliculas':dataset_per_director['Títtulos'].tolist(), 'anio':dataset_per_director['Fecha_de_Lanzamiento'].tolist(),
    'retorno_pelicula':dataset_per_director['Retorno'].tolist(), 
    'budget_pelicula':dataset_per_director['Presupuesto'].tolist(), 'revenue_pelicula':dataset_per_director['Recaudación'].tolist()}

#ML

#The creation of the data in rows 
#combined_features = (ml_data['genres_filtered']+ ' ').str.repeat(25)+ (ml_data['tagline'] + ' ').str.repeat(10) + (ml_data['cast_filtered'] + ' ').str.repeat(20) + (ml_data['crew_filtered']+' ').str.repeat(15)+(ml_data['production_companies_filtered']+' ').str.repeat(20)+(ml_data['overview']).str.repeat(10)
combined_features=ml_data['combined_features']

#vectorization
vectorizer = TfidfVectorizer()
feature_vectors=vectorizer.fit_transform(combined_features)

#Cosine similarity
similarity = cosine_similarity(feature_vectors)
movies_list= ml_data['title'].tolist()

@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    #Interaction with user
    movie_name=titulo
    #Closest match
    find_close_match = difflib.get_close_matches(movie_name, movies_list)

    #Closest match possible in the data
    close_match = find_close_match[0]
    id_of_the_movie = ml_data[ml_data.title == close_match]['id'].values[0]

    #Obtain the more similar movie
    similarity_score = list(enumerate(similarity[id_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 

    i = 1
    recommendation_movies = []
    added_movies = set()  # Utilizar un conjunto para rastrear las películas agregadas

    for movie in sorted_similar_movies:
        id = movie[0]
        filtered_df = ml_data[ml_data['id'] == id]
        if not filtered_df.empty:
            title_from_id = filtered_df['title'].values[0]
        if title_from_id not in added_movies:  # Verificar si la película ya está en la lista
            recommendation_movies.append(title_from_id)
            added_movies.add(title_from_id)  # Agregar la película al conjunto de películas agregadas
            i += 1
        if i >= 6:
            break  # Detener el bucle si se han agregado suficientes películas a la lista
    
    return {'lista recomendada': recommendation_movies}