import csv
import rdflib
from rdflib.namespace import RDF, RDFS, XSD

# Define los prefijos y espacios de nombres

# Crear grafo RDF vacío
g = rdflib.Graph()

tree = rdflib.Namespace("http://example.com/tree/")
g.bind("tree", tree)
geo = rdflib.Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
g.bind("geo", geo)
s = rdflib.Namespace("https://schema.org/")

g.add((tree.Tree, RDF.type, RDFS.Class))
g.add((tree.StreetTree, RDF.type, RDFS.Class))
g.add((tree.StreetTree, RDFS.subClassOf, tree.Tree))
g.add((tree.ParkTree, RDF.type, RDFS.Class))
g.add((tree.ParkTree, RDFS.subClassOf, tree.Tree))

# Leer archivo CSV y agregar datos al grafo RDF
with open('odTrees.csv',"r") as csvfile:
    reader = csv.DictReader(csvfile)
    i=0
    for i, row in enumerate(reader):
        if i >= 10000:
            break
        treeID = tree["tree" + str(i)]

        if (row["TYPEOFTREE"] == "StreetTree"):
            g.add((treeID, RDF.type, tree.StreetTree))
        elif (row["TYPEOFTREE"] == "ParkTree"):
            g.add((treeID, RDF.type, tree.ParkTree))
        g.add((treeID, tree.speciesType, rdflib.Literal(row["SPECIESTYPE"])))
        g.add((treeID, tree.species, rdflib.Literal(row["SPECIES"])))
        g.add((treeID, tree.age, rdflib.Literal(row["AGE"])))
        g.add((treeID, tree.description, rdflib.Literal(row["DESCRIPTION"])))
        g.add((treeID, tree.treeSurround, rdflib.Literal(row["TREESURROUND"])))
        g.add((treeID, tree.vigour, rdflib.Literal(row["VIGOUR"])))
        g.add((treeID, tree.condition, rdflib.Literal(row["CONDITION"])))
        g.add((treeID, tree.diameterInCentimeters, rdflib.Literal(row["DIAMETERinCENTIMETRES"], datatype=XSD.integer)))
        g.add((treeID, tree.spreadRadiusInMetres, rdflib.Literal(row["SPREADRADIUSinMETRES"], datatype=XSD.float)))
        g.add((treeID, geo.lat, rdflib.Literal(row["LATITUDE"], datatype=XSD.float)))
        g.add((treeID, geo.long, rdflib.Literal(row["LONGITUDE"], datatype=XSD.float)))
        g.add((treeID, tree.treeTag, rdflib.Literal(row["TREETAG"])))
        g.add((treeID, tree.treeHeightInMetres, rdflib.Literal(row["TREEHEIGHTinMETRES"], datatype=XSD.float)))

# Imprime el resultado en formato Turtle
with open('output.rdf', 'w') as f:
    f.write(g.serialize(format='turtle'))