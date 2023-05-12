import csv
import rdflib
from rdflib.namespace import RDF, RDFS, XSD

species = []
# Define los prefijos y espacios de nombres
with open('dbrSpecies.txt',"r") as file:
    Lines = file.readlines()
    for line in Lines:
        species.append(line.replace("\n",""))

# Crear grafo RDF vacío
g = rdflib.Graph()

tree = rdflib.Namespace("http://example.org/tree")
g.bind("tree", tree)
geo = rdflib.Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
g.bind("geo", geo, override=True)
qudt = rdflib.Namespace("https://qudt.org/2.1/vocab/unit")
g.bind("qudt", qudt)
dbr = rdflib.Namespace("http://dbpedia.org/resource/")
g.bind("dbr", dbr)

g.add((tree.StreetTree, RDF.type, RDFS.Class))
g.add((tree.ParkTree, RDF.type, RDFS.Class))

# Leer archivo CSV y agregar datos al grafo RDF
with open('odTrees.csv',"r") as csvfile:
    reader = csv.DictReader(csvfile)
    i=0
    for i, row in enumerate(reader):
        if i >= 100000:
            break
        treeID = tree["tree" + str(i)]

        if (row["SPECIES"].replace(" ","_") in species):
            if (row["TYPEOFTREE"] == "StreetTree"):
                g.add((treeID, RDF.type, tree.StreetTree))
            elif (row["TYPEOFTREE"] == "ParkTree"):
                g.add((treeID, RDF.type, tree.ParkTree))
            g.add((treeID, tree.speciesType, rdflib.Literal(row["SPECIESTYPE"])))
            g.add((treeID, RDF.type, getattr(dbr, row["SPECIES"].replace(" ","_"))))
            g.add((treeID, tree.age, rdflib.Literal(row["AGE"])))
            g.add((treeID, tree.description, rdflib.Literal(row["DESCRIPTION"])))
            g.add((treeID, tree.treeSurround, rdflib.Literal(row["TREESURROUND"])))
            g.add((treeID, tree.vigour, rdflib.Literal(row["VIGOUR"])))
            g.add((treeID, tree.condition, rdflib.Literal(row["CONDITION"])))
            g.add((treeID, tree.diameter, rdflib.Literal(float(row["DIAMETERinCENTIMETRES"])/100.0, datatype=XSD.float)))
            g.add((treeID, tree.spreadRadius, rdflib.Literal(row["SPREADRADIUSinMETRES"], datatype=XSD.float)))
            g.add((treeID, geo.lat, rdflib.Literal(row["LATITUDE"], datatype=XSD.float)))
            g.add((treeID, geo.long, rdflib.Literal(row["LONGITUDE"], datatype=XSD.float)))
            g.add((treeID, tree.treeTag, rdflib.Literal(row["TREETAG"])))
            g.add((treeID, tree.treeHeight, rdflib.Literal(row["TREEHEIGHTinMETRES"], datatype=XSD.float)))
            g.add((treeID, tree.units, qudt.m))

# Imprime el resultado en formato Turtle
with open('output.ttl', 'w') as f:
    f.write(g.serialize(format='turtle'))