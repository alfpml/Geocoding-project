# Geocoding-project

OBJETIVO
Voy a buscar la mejor localización en función de los requisitos listados debajo entre las coordenadas de las oficinas en el dataset de companies 

CRTERIOS
- Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design. => He seleccionado ciudades con otras empresas de gaming
- GUARDERAIAS: 30% of the company have at least 1 child. => He buscado colegios waldorf con Gmaps API
- RAISE MONEY: Developers like to be near successful tech startups that have raised at least 1 Million dollars.  => He seleccionado oficinas con más 50 empleados o que hayan tenido rondas de financiación con pymomgo y fundadas hace menos de 10 años
- STARBUCKS: Executives like Starbucks A LOT. Ensure there's a starbucks not to far.  => He buscado starbucks con Gmaps API
- AIRPORTS: Account managers need to travel a lot => He buscado starbucks con Gmaps API
- VEGAN RESTAURANTS: The CEO is Vegan => He buscado starbucks con Gmaps

CÓDIGO
I. Limpieza de datos ["filtered_offices.py", "airports.py"]

En "filtered_offices.py" limpio la base de datos de companies con pymongo hasta quedarme con 85 posibles oficinas en tres ciudades de US ("Redwood City","Boston","Austin") siguiendo estos pasos:

    ##find companies with more than 50 employees or having funding rounds with pymongo
    ##Filtering to US where most of the companies are and counting companies per city
    ##Filtering out cities with high concentration of startup companies (over 50) and with too low (below 20)
    ##selecting cities with at least two gaming companies

En "airports.py" de la base de datos de aeropuertos (csv) saco los US airports with over 40 direct flights para luego poder sacar el aeropuerto más cercano a las oficinas filtradas. 

Los resultados de estas limpiezas los guardo en 2 CSVs en la carpeta output ("filtered_offices.csv","filtered_airports.csv")

II Main.py

---------> Calcular distancia a Aeropuerto/starbucks/colegio/vegano más cercano
Empiezo desde los CSVs de aeropuertos y oficinas generados en el paso anterior que paso a dataframes. Partiendo de las 85 oficinas saco la distancia al aeropuerto más cercano (con geopy distance), al starbucks más cercano, al colegio waldorf más cercano y al restaurante vegano más cercano.


---------> Rankear en función de la cercanía
Para elegir la mejor localización de entre las 85 oficinas rankeo en función de las distancias a aeropuerto/starbucks/colegio/vegano más cercano y encuentro unas coordenadas en Cambridge (Boston). Con folium genero un mapa al que añado el starbucks/colegio/vegano más cercano y genero un  office_location.html en output folder.


III. Funciones

functions_search.py: funciones basadas en geopy.distance.geodesic y en la API de Places de GMAPs 
functions_rank.py: funciones para rankear (punto a mejorara sería tomar los valores para el rankeo como input) 
functions_mongo.py: funciones para cargar DB/collections de mongo



