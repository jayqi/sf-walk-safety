<!-- Leaflet Map -->

L.mapbox.accessToken = 'pk.eyJ1IjoianlxaSIsImEiOiJjaW01ZG11MjcwMWl0dGttM2R2c2JvbThiIn0.eE6Xt0dMIl7Y2tOT8e6dyQ';
var map = L.mapbox.map('map', 'mapbox.light')
.setView([37.7833, -122.4167], 12);

function getColor(d) {
    return d > 1500 ? '#800026' :
    d > 1250  ? '#BD0026' :
    d > 1000  ? '#E31A1C' :
    d > 750  ? '#FC4E2A' :
    d > 500   ? '#FD8D3C' :
    d > 250   ? '#FEB24C' :
    d > 100   ? '#FED976' :
                '#FFEDA0';
}
function style(feature) {
    return {
        fillColor: getColor(feature.properties.robcount),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

var geojson;

var info = L.control();
info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'mapinfo'); // create a div with a class "mapinfo"
    this.update();
    return this._div;
};
// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>Robbery Counts by Neighborhood</h4>' +  (props ?
        '<b>' + props.nhood + '</b><br />' + props.robcount + ' robberies'
        : 'Hover over a neighborhood');
};




function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }
    info.update(layer.feature.properties);
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}
function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}
function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}





geojson = L.geoJson(data, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(map);


info.addTo(map);





var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'mapinfo maplegend'),
        grades = [0, 100, 250, 500, 750, 1000, 1250, 1500],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(map);
