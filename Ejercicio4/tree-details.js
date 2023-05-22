// Obtener los parámetros de consulta de la URL
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

// Obtener los valores de los parámetros
const treeURI = urlParams.get('tree');
const tree = treeURI.split("/").slice(-1)[0];
console.log(tree);

fetch('http://156.35.98.70:3030/trees_ds/sparql', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: 'query=' + encodeURIComponent(`
        PREFIX schema: <http://schema.org/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> 
        PREFIX qudt: <https://qudt.org/2.1/vocab/unit> 
        PREFIX tree: <http://example.org/tree/> 
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?condition ?species ?description ?diameter ?spreadRadius ?height ?treeSurround ?type ?units ?vigour ?latitude ?longitude ?label ?age ?speciesDBR ?tag ?speciesType (SAMPLE(?image) AS ?sampleImage)
        WHERE {
            tree:${tree} tree:condition ?condition  ;
                         tree:species ?species  ;
                         tree:description ?description ;
                         tree:diameter ?diameter ;
                         tree:spreadRadius ?spreadRadius ;
                         schema:height ?height ;
                         tree:treeSurround ?treeSurround ;
                         tree:type ?type ;
                         tree:units ?units ;
                         tree:vigour ?vigour ;
                         geo:lat ?latitude ;
                         geo:long ?longitude .
            OPTIONAL {tree:${tree} tree:age ?age}
            OPTIONAL {tree:${tree} a ?speciesDBR}
            OPTIONAL {tree:${tree} tree:tag ?tag}
            OPTIONAL {tree:${tree} wdt:P31 ?speciesType
                SERVICE <https://query.wikidata.org/sparql> {
                    ?speciesType rdfs:label ?label
                    FILTER(LANG(?label) = "en")
                    ?speciesType wdt:P18 ?image
                }
            }
        }
        GROUP BY ?condition ?species ?description ?diameter ?spreadRadius ?height ?treeSurround ?type ?units ?vigour ?latitude ?longitude ?label ?age ?speciesDBR ?tag ?speciesType
`),
})
  .then(response => response.json())
  .then(data => {

    const results = data.results.bindings;
    for (const binding of results) {
        const condition = binding.condition.value;
        const species = binding.species.value;
        const description = binding.description.value;
        const diameter = binding.diameter.value;
        const spreadRadius = binding.spreadRadius.value;
        const height = binding.height.value;
        const treeSurround = binding.treeSurround.value;
        const type = binding.type.value;
        const units = binding.units.value.split("https://qudt.org/2.1/vocab/unit")[1];
        const vigour = binding.vigour.value;
        const latitude = parseFloat(binding.latitude.value);
        const longitude = parseFloat(binding.longitude.value);

        var age = "";
        var speciesDBR = "";
        var tag ="";
        var speciesType = "";
        var sampleImage = "";
        var treeLabel = "";


        if (binding.age) {
            age = binding.age.value;
        }
        
        if (binding.speciesDBR) {
            speciesDBR = binding.speciesDBR.value;
        }

        if (binding.tag) {
            tag = binding.tag.value;
        }

        if (binding.speciesType) {
            speciesType = binding.speciesType.value;
            sampleImage =binding.sampleImage.value;
            treeLabel = binding.label.value;
        }

        // Mostrar los detalles del árbol en la página
        const treeDetailsElement = document.getElementById('tree-details');
        treeDetailsElement.innerHTML = `
            <hgroup>
                <h2>${tree}</h2>
                <p><strong>Uri:</strong> ${treeURI}</p>
            </hgroup>
            <img src=${sampleImage} alt="${treeLabel}" onerror="this.onerror=null; this.alt='Image not found'">
            <p><strong>tag:</strong> ${tag}</p>
            <p><strong>Species Type:</strong> ${treeLabel} <a href="${speciesType}">${speciesType}</a></p>
            <p><strong>Species:</strong> ${species} <a href="${speciesDBR}">${speciesDBR}</a></p>
            <p><strong>Age:</strong> ${age}</p>
            <p><strong>Condition:</strong> ${condition}</p>
            <p><strong>Vigour:</strong> ${vigour}</p>
            <p><strong>Tree Surround:</strong> ${treeSurround}</p>
            <p><strong>Description:</strong> ${description}</p>
            <p><strong>Diameter:</strong> ${diameter} ${units}</p>
            <p><strong>Spread Radius:</strong> ${spreadRadius} ${units}</p>
            <p><strong>Height:</strong> ${height} ${units}</p>    
            <p><strong>Type:</strong> ${type}</p>
            <p><strong>Latitud:</strong> ${latitude}</p>
            <p><strong>Longitud:</strong> ${longitude}</p>
        `;
    }
  })
  .catch(error => console.error('Error:', error));