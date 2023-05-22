import csv
import rdflib
from rdflib.namespace import RDF, RDFS, XSD
import json

# Se leen los datos de las species de dbpedia y wikidata
species = []
speciesType = []

with open('dbrSpecies.txt',"r") as file:
    Lines = file.readlines()
    for line in Lines:
        species.append(line.replace("\n",""))

with open('wdtSpeciesType.json') as json_file:
    speciesType = json.load(json_file)

# Se crea el grafo y se añaden los espacios de nombres
g = rdflib.Graph()

tree = rdflib.Namespace("http://example.org/tree/")
g.bind("tree", tree)
geo = rdflib.Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
g.bind("geo", geo, override=True)
qudt = rdflib.Namespace("https://qudt.org/2.1/vocab/unit")
g.bind("qudt", qudt)
dbr = rdflib.Namespace("http://dbpedia.org/resource/")
g.bind("dbr", dbr)
wd = rdflib.Namespace("http://www.wikidata.org/entity/")
g.bind("wd", wd)
wdt = rdflib.Namespace("http://www.wikidata.org/prop/direct/")
g.bind("wdt", wdt)
schema = rdflib.Namespace("http://schema.org/")
g.bind("schema", schema)

# Para cada fila del csv se crea un árbol con los datos de cada columna (si existe el dato)
with open('odTrees.csv',"r") as csvfile:
    reader = csv.DictReader(csvfile)
    i=0
    for row in reader:
        treeID = tree["tree" + str(i)]
        g.add((treeID, tree.type, rdflib.Literal(row["TYPEOFTREE"])))
        if (row["SPECIESTYPE"] != "Mixed" and row["SPECIESTYPE"] != "N/A" and row["SPECIESTYPE"] != "Not Known"):
            g.add((treeID, wdt.P31, getattr(wd, speciesType[row["SPECIESTYPE"]])))
        if (row["SPECIES"].replace(" ","_") in species):
            g.add((treeID, RDF.type, getattr(dbr, row["SPECIES"].replace(" ","_"))))  
        if (row["AGE"] != ""):  
            g.add((treeID, tree.age, rdflib.Literal(row["AGE"])))
        g.add((treeID, tree.species, rdflib.Literal(row["SPECIES"])))  
        g.add((treeID, tree.description, rdflib.Literal(row["DESCRIPTION"])))
        g.add((treeID, tree.treeSurround, rdflib.Literal(row["TREESURROUND"])))
        g.add((treeID, tree.vigour, rdflib.Literal(row["VIGOUR"])))
        g.add((treeID, tree.condition, rdflib.Literal(row["CONDITION"])))
        g.add((treeID, tree.diameter, rdflib.Literal(float(row["DIAMETERinCENTIMETRES"])/100.0, datatype=XSD.float)))
        g.add((treeID, tree.spreadRadius, rdflib.Literal(row["SPREADRADIUSinMETRES"], datatype=XSD.float)))
        g.add((treeID, geo.lat, rdflib.Literal(row["LATITUDE"], datatype=XSD.float)))
        g.add((treeID, geo.long, rdflib.Literal(row["LONGITUDE"], datatype=XSD.float)))
        if (row["TREETAG"] != ""): 
            g.add((treeID, tree.tag, rdflib.Literal(row["TREETAG"])))
        g.add((treeID, schema.height, rdflib.Literal(row["TREEHEIGHTinMETRES"], datatype=XSD.float)))
        g.add((treeID, tree.units, qudt.m))
        i+=1

# Se guarda el resultado en formato Turtle
with open('output.ttl', 'w') as f:
    f.write(g.serialize(format='turtle'))