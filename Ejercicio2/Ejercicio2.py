from pyshex import ShExEvaluator, PrefixLibrary

# Se lee el archivo de validación
shexFile = open("validatorSHEX.shex", "r")
schema = shexFile.read()
shexFile.close()


# Se leen los datos en ttl obtenidos en el Ejercicio 1
ttlFile = open("output.ttl", "r")
ttl = ttlFile.read()
ttlFile.close()

# Se cargan los prefijos
p = PrefixLibrary(ttl)

# Se inician las variables para contar el número de elementos validados
passCount = 0
failCount = 0

for result in ShExEvaluator(rdf=ttl, schema=schema, start=p.TREE.Tree).evaluate():
    if result.result:
        passCount += 1
    else:
        failCount += 1
        print(f"{result.focus}: Failing")
        print(result.reason)

print("Number of trees passing validation:", passCount)
print("Number of trees failing validation:", failCount)