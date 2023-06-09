from fastapi import FastAPI

#Importing the libraries
import pandas as pd
import calendar 

#import the data
data= pd.read_csv('datasets\DEset.csv')
df = pd.DataFrame(data)
df.drop_duplicates(subset='id',inplace=True)

credits=pd.read_csv('datasets\credits_filtered.csv')
df_credits=pd.DataFrame(credits)

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
def cantidad_filmaciones_mes(Mes):
    errormessage = 'Has ingresado un nombre de mes inválido, intenta otra vez ingresando el nombre del mes en español y sin ", gracias.'
    meses_validos = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    
    if Mes.lower() not in meses_validos:
        return errormessage

    No_mes = meses_validos.index(Mes.lower()) + 1
    
    df_mes = df[df['release_date'].dt.month == No_mes]
    No_peliculas = len(df_mes)

    return "{} película fueron estrenadas en el mes {}".format(No_peliculas,Mes)

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
def cantidad_filmaciones_dia(Dia):
    errormessage = 'Has ingresado un nombre de día inválido, intenta otra vez'
    dias_validos = ['lunes', 'martes', 'miércoles', 'jueves','viernes','sábado', 'domingo']
    
    if Dia.lower() not in dias_validos:
        return errormessage
    
    day=convertir_dia(Dia.lower())
    
    df_dia = df[df['release_date'].dt.strftime("%A") == day]
    No_peliculas = len(df_dia)

    return "{} películas fueron estrenadas en  {}".format(No_peliculas,Dia)

#Films by title 

@app.get("/score_titulo/{titulo}")
def score_titulo(titulo):
    df_titulo = df[df['title'] == titulo]
    df_titulo.drop(['Unnamed: 0', 'budget', 'id', 'original_language', 'overview',
        'release_date', 'revenue', 'runtime', 'status', 'tagline',
        'vote_average', 'vote_count', 'genres_filtered',
       'spoken_languages_filtered', 'production_companies_filtered',
       'production_countries_filtered', 'belongs_to_collection_filtered',
        'return'], axis=1,inplace=True)

    year= int(df_titulo['release_year'])
    popularity=float(df_titulo['popularity'])

    return "{} fue estrenada en {} siendo rankeada en popularidad con {}".format(titulo, year, popularity)

#Films by title and the votes

@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo):
    df_titulo = df[df['title'] == titulo]
    df_titulo.drop(['Unnamed: 0', 'budget', 'id', 'original_language', 'overview',
        'release_date', 'revenue', 'runtime', 'status', 'tagline',
        'popularity', 'genres_filtered', 'spoken_languages_filtered', 
        'production_companies_filtered', 'production_countries_filtered', 
        'belongs_to_collection_filtered','return'], axis=1,inplace=True)

    year= int(df_titulo['release_year'])
    vote_count= int(df_titulo['vote_count'])
    vote_average=float(df_titulo['vote_average'])

    if vote_count>=2000:
        return "{} fue estrenada en {} siendo contando con un total de valores de {} con un promedio de {}".format(titulo, year, vote_count,vote_average)
    else:
        return "{} no contó con un mínimo de 2000 valoraciones".format(titulo)
    
#Films by the cast

def get_ids_cast(name):
    ids = []
    for cast_list in df_credits['cast_filtered']:
        if name in cast_list:
            ids.append(df_credits.loc[df_credits['cast_filtered'] == cast_list, 'id'].to_list())

    result = [num for sublist in ids for num in sublist]

    return result

@app.get("/get_actor/{name}")
def get_actor(name):
    total_return=0
    ids_films= get_ids_cast(name)

    for id in ids_films:
        if id in df['id'].values:
            total_return += float(df.loc[df['id'] == id, 'return'])
    
    total_films=len(ids_films)
    average_return=total_return/total_films

    return "{} ha obtenido un retorno de {} gracias a su participación en {} películas, dando un promedio por films de {} ".format(name, total_return,total_films,average_return)


#Films by the director

df_credits.fillna('No Director Info',inplace=True)

def get_ids_crew(name):
    ids = []
    for i in range(df_credits.shape[0]):
        if name == df_credits['crew_filtered'].iloc[i]:
            ids.append(df_credits['id'].iloc[i])

    return ids

@app.get("/get_director/{name}")
def get_director(name):
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

    message="{} ha obtenido un retorno de {}".format(name, total_return)
    Nota= "la información a la izquierda corresponde al ID registrado, puede ser usado para verificar la información del film en específico"
    return message, Nota, dataset_per_director.head(rows)
