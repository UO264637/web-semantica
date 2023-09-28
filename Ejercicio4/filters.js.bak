// Creación del mapa
const map = L.map('map').setView([54.5970, -5.9300], 11);
var markersLayer = L.layerGroup().addTo(map);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
    }).addTo(map);


// JSON de tipos de especie
const speciesData = {
    "Alder":"Q25239",
    "Amelanchier":"Q156957",
    "Apple":"Q18674606",
    "Ash":"Q156907",
    "Beech":"Q59779138",
    "Birch":"Q25243",
    "Cedar":"Q128550",
    "Cherry":"Q62474322",
    "Chestnut":"Q129324",
    "Cotoneaster":"Q5538",
    "Crab Apple":"Q47161",
    "Cypress":"Q146911",
    "Elder":"Q22701",
    "Elm":"Q59779164",
    "Eucalyptus":"Q45669",
    "False Acaia":"Q157417",
    "Fir":"Q25350",
    "Gingko":"Q43284",
    "Handkerchief":"Q18348215",
    "Hawthorn":"Q132557",
    "Hazel":"Q124969",
    "Holly":"Q117085",
    "Hornbeam":"Q59779148",
    "Irish Yew":"Q110767650",
    "Juniper":"Q26325",
    "Laburnum":"Q147184",
    "Larch":"Q61996280",
    "Lawson Cypress":"Q161360",
    "Lime":"Q45417383",
    "Liquidamber":"Q183543",
    "Magnolia":"Q157017",
    "Maple":"Q42292",
    "Oak":"Q12004",
    "Pear":"Q434",
    "Pine":"Q12024",
    "Plane":"Q157739",
    "Plum":"Q6401215",
    "Poplar":"Q30456678",
    "Rauli":"Q1317892",
    "Redwood":"Q1975652",
    "Rowan":"Q157964",
    "Spruce":"Q26782",
    "Sweet Chestnut":"Q22699",
    "Tree Of Heaven":"Q159570",
    "Tulip":"Q158783",
    "Walnut":"Q46871",
    "Western Hemlock":"Q1144409",
    "Willow":"Q36050",
    "Yew":"Q27355",
    "Yucca":"Q156317"
  }
  
  const selectedValues = [];
  const filterList = document.getElementById('filter-list');
  

  for (const species in speciesData) {
    const listItem = document.createElement('li');
    
    // Crear el checkbox
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.value = speciesData[species];
    if (species == "Gingko"){
        checkbox.checked = true;
        selectedValues.push(speciesData[species]);
        query(selectedValues);
    }
    checkbox.autocomplete='off';

    checkbox.addEventListener('change', () => { // Añade o elimina el filtro de la lista y llama a la consulta
        const value = checkbox.value;
        
        if (checkbox.checked) {
          selectedValues.push(value);
        } else {
          const index = selectedValues.indexOf(value);
          if (index > -1) {
            selectedValues.splice(index, 1);
          }
        }
        query(selectedValues);
      });
    
    // Crear la etiqueta del checkbox
    const label = document.createElement('label');
    label.textContent = " "+ species;
    label.setAttribute('for', speciesData[species]);
    
    listItem.appendChild(checkbox);
    listItem.appendChild(label);
    filterList.appendChild(listItem);
  }
  
  //Obtiene los árboles de los filtros marcados (el límite es 1000 porque si no se ralentiza mucho el navegador)
  function query(selectedValues) {
    const valuesStr = selectedValues.map(value => `wd:${value}`).join(', ');

    fetch('http://156.35.98.70:3030/trees_ds/sparql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'query=' + encodeURIComponent(`
                PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                PREFIX wd: <http://www.wikidata.org/entity/>

                SELECT ?tree ?latitude ?longitude 
                WHERE {
                    ?tree geo:lat ?latitude ;
                        geo:long ?longitude .
                    ?tree wdt:P31 ?speciesType .
                    FILTER (?speciesType IN (${valuesStr}))
                }
                LIMIT 1000
        `),
    })
  .then(response => response.json())
  .then(data => {
    markersLayer.clearLayers(); // Elimina marcas anteriores del mapa
    // Cambia los marcadores por defecto del mapa por iconos de árbol
    const treeIcon = L.icon({
        iconUrl: './resources/tree-icon.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
        iconSize: [35, 40],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      });

    const results = data.results.bindings;
    for (const binding of results) { // Crea una marca para cada árbol y le añade un popup con un enlace a más detalles
        const treeURI = binding.tree.value;
        const latitude = parseFloat(binding.latitude.value);
        const longitude = parseFloat(binding.longitude.value);

        const marker = L.marker([latitude, longitude], { icon: treeIcon }).addTo(markersLayer);

        const content = `
          <div>
            <h3>${treeURI}</h3>
            <p>Latitude: ${latitude}</p>
            <p>Longitud: ${longitude}</p>
            <a href=tree-details.html?tree=${treeURI}>View Details</a>
          </div>
        `;

        marker.bindPopup(content);
    }
  })
  .catch(error => console.error('Error:', error));
  }