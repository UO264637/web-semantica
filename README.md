# Web Semántica - MIW 2023

Enlace al vídeo: https://youtu.be/_zIebe7ZE5I

## Ejercicio 1
 En la carpeta del ejercicio 1 se encuentra el código fuente y todos los archivos necesarios para su ejecución (los datos originales odTrees.csv junto con dbrSpecies.txt y wdtSpeciesType.json que contienen las especies de árboles de dbpedia y los identificadores de wikidata respectivamente).
 
 Como había demasiadas especies para buscar cada uno de sus identificadores en wikidata, copié todas las especies de dbpedia en un txt y añadí las que coincidían con la especie del árbol. Para los tipos de specie, como eran menos, sí que utilicé los identificadores de wikidata que se encuentran en un .json.
 
 He elegido unos datos sobre los árboles de Belfast en .csv y el programa que los pasa a RDF está hecho en Python v3.11.3.
 - Datos elegidos: https://data.europa.eu/data/datasets/belfast-trees?locale=es
 - Ejecución: 
   - pip install rdflib 
   - python Ejercicio1.py

He incluido los datos en dos almacenes RDF
 - Fuseki: http://156.35.98.70:3030/#/
 - BlazeGraph: http://156.35.98.69:9999/blazegraph/#splash
 
 (Acceder a ambos desde la red de uniovi o con VPN)
 
## Ejercicio 2
 En la carpeta del ejercicio 2 se pueden encontrar los validadores en ShEx y SHACL para los árboles anteriores. También hay un programa en Python que valida automáticamente todos estos datos utilizando la librería pyShEx. Seguí el ejemplo de: https://github.com/hsolbrig/PyShEx/blob/master/notebooks/school_example.ipynb

 Es necesario que el archivo output.ttl del ejercicio 1 y validationSHEX.shex se encuentren en el mismo directorio.
  - Ejecución: 
    - pip install pyshex  
    - python Ejercicio2.py
  
## Ejercicio 3
 En la carpeta del ejercicio 3 se pueden encontrar todas las consultas realizadas en un fichero junto con los datos obtenidos tras su ejecución.
 
 Las consultas federadas de wikidata tardan bastante tiempo en ejecutarse, unos 15-20 minutos.
 
 ## Ejercicio 4
 En la carpeta dele ejercicio 4 se puede encontrar el código y archivos necesarios para ejecutar la aplicación web, para ello solo hay que abrir index.html en un navegador. También se puede encontrar desplegada en: http://156.35.98.70/WebSemantica/Ejercicio4/
 
 La aplicación cuenta con las siguientes funcionalidades:
  - Mapa donde se muestran los árboles.
  - Filtros de árboles por tipo de especie. Como la consulta de wikidata tarda mucho tiempo en ejecutarse he incluido las especies de árbol en el código directamente en JSON. He limitado a 1000 el número de árboles de cada especie que se representan en el mapa para evitar que se ralentice demasiado el navegador.
  - Al pasar el ratón por los distintos árboles del mapa se muestra un pequeño cuadro con la información básica del árbol y un enlace para ver todos los detalles.
  - Página de detalles del árbol. Muestra toda la información del árbol, incluida la imagen asociada a su tipo de especie de wikidata si la hubiera.
