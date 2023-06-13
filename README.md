<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>
# <h1 align=center> **Ricardo Castro Peraza** </h1>
# <h1 align=center> **Cohorte:11** </h1>


# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300>
</p>

Es indudable el éxito rotundo de las plataformas de streaming tales como *Netflix* y *Disney +* a raíz del confinamiento por la pandemia del COVID-19, las personas han cambiado su rutina pasando una mayor cantidad de tiempo en el hogar, siendo estas plataformas irremplazables compañeros que, entre otras actividades, se encargan de proveer contenido de calidad y sobre todo, personalizado al usuario. 

El actual proyecto contiene distintos distintos entregables: 
+ *`Transformaciones`* : Donde se generan cambios en la un dataframe que contiene información de películas utilizando la librería pandas de acuerdo a requerimentos precisos. 

+ *`Desarrollo API`* : Donde se generan 6 funciones con interacción de usuario que extraen información sobre películas de acuerdo al mes o día de publicación, al titulo retornando información como la recaudación del film o introduciendo el nombre de un director o actor que haya participado para extraer información sobre los films donde ha estado. Esta información se entrega como un diccionario siendo capaz de consumirse como formato json y se encuentra disponible para su consumo en la web.

+ *`Análisis Exploratorio de Datos`* : Para la generación de un modelo de *Machine Learning* (en adelante, *ML*), se realizó un análisis de los datos donde se corroboró y verificó el compartiendo de variables numéricas como la recaudación, votos promedios, presupuestos y duración de películas del dataset. De igual manera, se generó una nube de palabras para observar la tendencia en los productos más populares en cuestión de temática por su frecuencia de palabras en títulos y la descripción. 

+ *`Sistema de Recomendación de Películas`* : Mediante la manipulación con la función  **recomendacion( *`titulo`* )**, el usuario obtiene una lista de 5 películas incluida la que introdujo. Los fundamentos teórico-prácticos del sistema son descritos posteriormente. 


El objetivo fue el deploy de la API conteniendo las 6 funciones relacionadas a la extracción de información del archivo de películas y la función asociada al modelo de *ML*. y siendo desarrolladas en *Python 3.11.0* y se empleó el sitio web *render.com* para el deploy de la *API*. 

*`Palabras Clave`*: sistema de recomendación, *machine learning*, *API*, ciencia de datos, ingeniería de datos, análisis exploratorio de datos
<hr>  

## **Introducción**

### Modelos de Recomendación

La información filtrada que cumple el objetivo de predecir la preferencia del usuario ha revolucionado el estilo de busquedas de los interéres (Kumar et. *al*, 2015)

La experiencia del usuario se ha converntido en uno de los pilares de negocio en la nueva generación, los sistemas de recomendación vienen a guíar al usuario sobre el consumo de su preferencia siendo aplicables a distintas áreas como libros, CDs, series, destinos turísticos, productos para el hogar, museos y películas.  (Kumar et. *al*, 2015)

Compañías como *Netflix*, *Amazon*, y *Google* incorporan sistemas de recomendación y han reportado diferentes parámetros que evidencían el beneficio. (Kumar et. *al*, 2015) *Netflix* informa en el 2015, que aproximadamente 66% de las películas consumidas son a raíz de las recomendaciones, *Google* en su *branch* *Google News* experimentó un aumento del 38% de *clicks* en sus noticias por las recomendaciones, *Amazon* por su parte comenta que el 35% de sus ventas son gracias a la implementación de estos sitemas. (Kumar et. *al*, 2015)

El beneficio a raíz de la implementación de esta experiencia de usuario ha beneficiado al usario al reducir el tiempo de selección de productos en tiendas en línea, reduciendo la carga de información que no es de su agrado,  contribuyendo a la toma de decisiones y teniendo menor número de opciones, en comparación a una búsqueda tradicional, siendo posible considerar la mejor calidad del producto. (Phorasin, et *al.*, 2017)

Los sistemas de recomendación se componen de 4 partes: la base de datos que contiene información del producto, la interface humano-computadora, algoritmo de recomendación y componentes de recomendación. (Phorasin, et *al.*, 2017)

[![Base-de-datos.png](https://i.postimg.cc/L640pvgv/Base-de-datos.png)](https://postimg.cc/14TK0GHN)
<sub>*Figura 1. Componentes de la recomendación*<sub>

Existe una clasificación de los sistemas de recomendación en 2 categorías  (Kumar et. *al*, 2015):
+  Sistema de recomendación con enfoque colaborativo
+  Sistema de recomendación con enfoque de contenido

El enfoque colaborativo (CF) se basa en *ratings* o comportamientos de otros usuarios en el sistema conforme a la opinión de otros usuarios genera una predicción razonable para el consumo de otro usuario. (Phorasin, et *al.*, 2017). El enfoque de contenido (CBF) se basa en la similitud textual de la metadata contenida en la base de datos siendo, usualmente, tratada mediante la ténica de similitud de coseno que consta de 3 partes: ajuste de similtud de coseno, similitud basada en coseno y similitud basada en la correlación. (Phorasin, et *al.*, 2017)

La similitud de coseno mide la similitud de dos vectores obtenido de un producto interior en el coseno entre ellos. (Rojas, et *al.*, 2016) Por definición, la función trigonométrica coseno devuelve un valor de 1 cuando el ángulo evaluado es 0, suponiendo un ángulo ortogonal el valor obtenido sería de -1, de manera que la similitud de coseno se encuentra [-1,1]. (Rojas, et *al.*, 2016) En minería de datos, esta medida es empleada para poder comprobar la similitud entre textos y como cohesión entre clústers.

## **Metodología**

### Requerimientos del sistema
Se instaló los siguientes librerías en un entorno virtual de *Python*.
+ anyio==3.7.0
+ click==8.1.3
+ colorama==0.4.6
+ fastapi==0.96.0
+ h11==0.14.0
+ idna==3.4
+ joblib==1.2.0
+ numpy==1.21.6
+ pandas==1.3.5
+ pydantic==1.10.9
+ python-dateutil==2.8.2
+ pytz==2023.3
+ scikit-learn==1.0.2
+ scipy==1.7.3
+ six==1.16.0
+ sniffio==1.3.0
+ starlette==0.27.0
+ threadpoolctl==3.1.0
+ typing_extensions==4.6.3
+ tzdata==2023.3
+ uvicorn==0.22.0


### Prepocesamiento de datos

*`Transformaciones`*  se generaron las siguientes modificaciones:
+ Desanidación de **`belongs_to_collection`**, **`production_companies`**, **`production_countries`**, **`genres`**, **`spoken_languages`**, **`cast`** y **`crew`**. Mediante la implementación de la librería ast y su función literal eval comprobando la información y obteniendo el valor asociado a la clave *name* de los diccionarios presentes en cada fila de las columnas mencionadas

+ Rellenado de 0 a valores nulos en  **`revenue`** y **`budget`** .
  
+ Eliminación **`release date`** deben eliminarse donde se encuentren valores nulos

+ Reestructuración de formato de **`release date`** a **`AAAA-mm-dd`**.

+ Creación de la columna **`release_year`** donde extraerán el año de la fecha de estreno.

+ Creación de la columna **`return`** con los campos **`revenue`** y **`budget`**, dividiendo estas dos últimas **`revenue / budget`**, cuando no hay datos disponibles para calcularlo, deberá tomar el valor **`0`**.

+ Eliminación de  **`video`**,**`imdb_id`**,**`adult`**,**`original_title`**,**`poster_path`** y **`homepage`**.
<br/>

**`Desarrollo API`**: Se empleó la librería FastAPI 0.96.0 y uvicorn 0.22.0 para el desarrollo de 6 funciones:
  
+ def **cantidad_filmaciones_mes( *`Mes`* )**:
    Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.

+ def **cantidad_filmaciones_dia( *`Dia`* )**:
    Se ingresa un día en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.

+ def **score_titulo( *`titulo_de_la_filmación`* )**:
    Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.

+ def **votos_titulo( *`titulo_de_la_filmación`* )**:
    Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.

+ def **get_actor( *`nombre_actor`* )**:
    Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno.

+ def **get_director( *`nombre_director`* )**:
    Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.
<br/>

Es importante considerar que acepta nombres sin comillas para la correcta función de la API que se realizó el deploy en *render.com* siendo posible para su consumo en https://deploy-rcastroperaza-proyecto-individual.onrender.com

<br/>

**`Análisis exploratorio de los datos`**: _(Exploratory Data Analysis, EDA): Se revisó el comportamiento de variables numéricas, mismas que fueron corregidas de acuerdo a errores corroborados con base en la información provista por https://www.themoviedb.org/. Aquellos valores que tenían un porcentaje de nulos mayor a 80% fueron retiradas del modelo de acuerdo a la figura 2. 

[![Captura-de-Pantalla-2023-06-13-a-la-s-8-24-45-a-m.png](https://i.postimg.cc/d088Dkhn/Captura-de-Pantalla-2023-06-13-a-la-s-8-24-45-a-m.png)](https://postimg.cc/hJtJ5Gb7)
<sub>*Figura 2. Porcentaje de nulos en cada columna*<sub>

Con base en lo anterior expuesto se eliminaron **tagline* y **belongs_to_collections_filtered** que provenía del paso de **Transformación**. 

Posteriormente, se realizon análisis valores atípicos empleando diagramas de cajas y bigotes como se muestran en las figuras 3 y 4. 

[![graficas.jpg](https://i.postimg.cc/gJh9rLQM/graficas.jpg)](https://postimg.cc/tZ9vMJXP)

<sub>*Figura 3. Diagramas de cajas y bigotes para ls variables Recaudación, Duración, Presupuesto, Retorno y Popularidad*<sub>

[![Base-de-datos-3.jpg](https://i.postimg.cc/RVcrv99m/Base-de-datos-3.jpg)](https://postimg.cc/w7T4kC74)
<sub>*Figura 4. Diagramas de cajas y bigotes para las variables Promedio de votos y cantidad de votos*<sub>

De igual manera se generó un *bag of words* con los títulos de los films más populares como se ilustra en la figura 5.

[![bagofwords.png](https://i.postimg.cc/FH59xDFr/bagofwords.png)](https://postimg.cc/PPysXb89)
<sub>*Figura 5. Nubes de palabras con la variable **title***<sub>

**`Sistema de recomendación`**:  El sistema de recomendación está construido con base en un filtro híbrido. Debido a limitaciones en el almacenamiento se decidió depurar la base de datos más recomendadas a aquellas películas que cumplían con un mínimo de promedio de votos de 5 y una cantidad mínima de votos de 250. Con el filtrado anterior se generó un total de 3325 películas que serían las "más populares", siendo uno de los elementos del filtro colaborativo, posteriormenta para la construcción del modelo se utilizó una similtud de coseno de las variables **cast**, **director** (*crew* para el caso del código), **tagline**, **overview**, **production_company**, **genre** siendo evaluadas de acuerdo a la importancia descrita a continuación: 

+ Importancia del género: 25/100
+ Importancia de tagline: 10/100
+ Importancia del cast: 20/100
+ Importancia del director: 15/100
+ Importancia de la compañía productora: 20/100
+ Importancia del overview: 10/100

Previo a la vectorización se generó repeticiones de estas variables de manera proporcional al procentaje implementado de "importancia" de cada *feature*. El objetivo del anterior paso, fue mejorar el *performance* del sistema de recomendación dando mayor prioridad al género, cast y la compañía productora porque, debido a revisiones en literatura, son las variables más importantes en la toma de decisiones de consumidores sobre que película ver. 

Para concluir, se generó la función descrita a continuación:

+ def **recomendacion( *`titulo`* )**:
    Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.

<br/>

## **Fuente de datos**

+ [Dataset](https://drive.google.com/drive/folders/1nvSjC2JWUH48o3pb8xlKofi8SNHuNWeu): Carpeta con los 2 archivos con datos que requieren ser procesados (movies_dataset.csv y credits.csv)
+ [Diccionario de datos](https://docs.google.com/spreadsheets/d/1QkHH5er-74Bpk122tJxy_0D49pJMIwKLurByOfmxzho/edit#gid=0): Diccionario con algunas descripciones de las columnas disponibles en el dataset.
<br/>

## **Bibliografía**
+ Kumar, M., Yadav, D., Singh, A. y Gupta, V. (2015). A Movie Recommender System: MOVREC. International Journal of Computer Applications. 124(3)

+ Phongsavanh, P. y Lasheng Y. (2017). Movies Recommendation system using collaborative filtering and k-means. Internal Journal of Advanced Computer Research. 7(129)

+ Rojas Hernandez, A. F., y Gelvez Garcia, N. Y. (2016). Distributed processing using cosine similarity for mapping Big Data in Hadoop. IEEE Latin America Transactions, 14(6), 2857–2861. doi:10.1109/tla.2016.7555265 

<br/>