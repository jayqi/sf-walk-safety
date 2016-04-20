<!-- Leaflet Map -->

L.mapbox.accessToken = 'pk.eyJ1IjoianlxaSIsImEiOiJjaW01ZG11MjcwMWl0dGttM2R2c2JvbThiIn0.eE6Xt0dMIl7Y2tOT8e6dyQ';
var map = L.mapbox.map('map', 'mapbox.light')
.setView([37.7680, -122.4367], 12);

map.scrollWheelZoom.disable();

function getColor(d) {
    return d > {{mapdata['colorbar'][7] | safe}} ? '#b10026' :
    d > {{mapdata['colorbar'][6] | safe}}  ? '#e31a1c' :
    d > {{mapdata['colorbar'][5] | safe}}  ? '#fc4e2a' :
    d > {{mapdata['colorbar'][4] | safe}}  ? '#fd8d3c' :
    d > {{mapdata['colorbar'][3] | safe}}   ? '#feb24c' :
    d > {{mapdata['colorbar'][2] | safe}}   ? '#fed976' :
    d > {{mapdata['colorbar'][1] | safe}}   ? '#ffeda0' :
                '#ffffcc';
}
function style(feature) {
    return {
        fillColor: getColor(feature.properties.count),
        weight: 2,
        opacity: 1,
        color: '#CCCCCC',
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
    this._div.innerHTML = '<h4>{{pageopts['uppercase'] | safe}} Counts by {{ regionopts["uppercase"] | safe }}</h4>' +  (props ?
        '<b>' + props.{{ regionopts["key"] | safe }} + '</b><br />' + props.count + ' {{pageopts['lowercase'] | safe}}'
        : 'Hover over a {{regionopts["lowercase"] | safe}}');
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
        grades = {{ mapdata['colorbar'] | safe }},
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length-1; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + '&ndash;' + grades[i + 1] + '<br>';
            //grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(map);
