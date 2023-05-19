fetch('http://156.35.98.70:3030/trees_ds/sparql', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: 'query=' + encodeURIComponent(`
        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?tree ?latitude ?longitude ?label ?image
        WHERE {
            ?tree geo:lat ?latitude ;
                  geo:long ?longitude .
            ?tree wdt:P31 ?speciesType .
            SERVICE <https://query.wikidata.org/sparql> {
                ?speciesType rdfs:label ?label .
                FILTER(LANG(?label) = "en")
            }
        }
        LIMIT 200
`),
})
  .then(response => response.json())
  .then(data => {
    //console.log(JSON.stringify(data))

    const map = L.map('map').setView([54.5970, -5.9300], 11);

    // Agregar capa de mapa base
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    const greenIcon = L.icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      });

    const results = data.results.bindings;
    for (const binding of results) {
        const treeURI = binding.tree.value;
        const treeLabel = binding.label.value;
        const latitude = parseFloat(binding.latitude.value);
        const longitude = parseFloat(binding.longitude.value);

        const marker = L.marker([latitude, longitude], { icon: greenIcon }).addTo(map);

        // Agregar información adicional al marcador (opcional)
        marker.bindPopup(`<b>Árbol:</b> ${treeURI}<br><b>Tipo:</b> ${treeLabel}<br><b>Latitud:</b> ${latitude}<br><b>Longitud:</b> ${longitude}`);
    }
  })
  .catch(error => console.error('Error:', error));

