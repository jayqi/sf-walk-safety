<!-- Leaflet Map -->

L.mapbox.accessToken = 'pk.eyJ1IjoianlxaSIsImEiOiJjaW01ZG11MjcwMWl0dGttM2R2c2JvbThiIn0.eE6Xt0dMIl7Y2tOT8e6dyQ';
var map = L.mapbox.map('map', 'mapbox.light',{
    minZoom:12,
    maxZoom:18
})
    .setView([37.7680, -122.4367], 12);

map.scrollWheelZoom.disable();

// Log version: Function that assigns colors
function getColor_log(d) {
    return d >= {{mapdata['colorbar']['log'][8] | safe}} ? '#800026' :
    d >= {{mapdata['colorbar']['log'][7] | safe}} ? '#b10026' :
    d >= {{mapdata['colorbar']['log'][6] | safe}}  ? '#e31a1c' :
    d >= {{mapdata['colorbar']['log'][5] | safe}}  ? '#fc4e2a' :
    d >= {{mapdata['colorbar']['log'][4] | safe}}  ? '#fd8d3c' :
    d >= {{mapdata['colorbar']['log'][3] | safe}}   ? '#feb24c' :
    d >= {{mapdata['colorbar']['log'][2] | safe}}   ? '#fed976' :
    d >= {{mapdata['colorbar']['log'][1] | safe}}   ? '#ffeda0' :
                '#ffffcc';
};

// Linear version: Function that assigns colors
function getColor_lin(d) {
    return d >= {{mapdata['colorbar']['lin'][7] | safe}} ? '#800026' :
    d >= {{mapdata['colorbar']['lin'][6] | safe}} ? '#b10026' :
    d >= {{mapdata['colorbar']['lin'][5] | safe}}  ? '#e31a1c' :
    d >= {{mapdata['colorbar']['lin'][4] | safe}}  ? '#fc4e2a' :
    d >= {{mapdata['colorbar']['lin'][3] | safe}}  ? '#fd8d3c' :
    d >= {{mapdata['colorbar']['lin'][2] | safe}}   ? '#feb24c' :
    d >= {{mapdata['colorbar']['lin'][1] | safe}}   ? '#fed976' :
    d >= {{mapdata['colorbar']['lin'][0] | safe}}   ? '#ffeda0' :
                '#ffffcc';
};

// Function that styles the feature polygons
function style_log(feature,scaletype) {
    return {
        fillColor: getColor_log(feature.properties.count,scaletype),
        weight: 2,
        opacity: 1,
        color: '#CCCCCC',
        fillOpacity: 0.7
    };
};
function style_lin(feature,scaletype) {
    return {
        fillColor: getColor_lin(feature.properties.count,scaletype),
        weight: 2,
        opacity: 1,
        color: '#CCCCCC',
        fillOpacity: 0.7
    };
};

// Initialize geojson data
var loglayer;
var linlayer;


// Infobox
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

// Functionality to highlight feature
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

function resetHighlight_log(e) {
    loglayer.resetStyle(e.target);
    info.update();
}
function resetHighlight_lin(e) {
    linlayer.resetStyle(e.target);
    info.update();
}
function onEachFeature_log(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight_log,
        click: highlightFeature
    });
}
function onEachFeature_lin(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight_lin,
        click: highlightFeature
    });
}


var loglayer = L.geoJson(data, {
    style: style_log,
    onEachFeature: onEachFeature_log
})
var linlayer = L.geoJson(data, {
    style: style_lin,
    onEachFeature: onEachFeature_lin
});

// Add data to map
geojson = loglayer.addTo(map);


// Add infobox to map
info.addTo(map);




// Layer control
var choroplethlayers = {
    "Log": loglayer,
    "Linear": linlayer
};
L.control.layers(choroplethlayers).addTo(map);



var legend_log = L.control({position: 'bottomright'});
legend_log.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'mapinfo maplegend'),
        grades = {{ mapdata['colorbar']['log'] | safe }},
        labels = [];

    div.innerHTML = 'Log color scale: <br>'
    for (var i = 0; i < grades.length-1; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor_log(grades[i] + 1,'log') + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + (grades[i + 1]-1) + '<br>' : '');
    }
    div.innerHTML += '<i style="background:' + getColor_log(grades[grades.length-1] + 1,'log') + '"></i> ' + grades[grades.length-1]

    return div;
};


var legend_lin = L.control({position: 'bottomright'});

legend_lin.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'mapinfo maplegend'),
        grades = {{ mapdata['colorbar']['lin'] | safe }},
        labels = [];

    div.innerHTML = 'Linear color scale: <br>'
    // loop through our density intervals and generate a label with a colored square for each interval

    for (var i = 0; i < grades.length-1; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor_lin(grades[i] + 1) + '"></i> ' +
            grades[i] + '&ndash;' + grades[i + 1] + '<br>';
            //grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};




legend_log.addTo(map);

// Toggle legend when baselayer changes
map.on('baselayerchange', function (eventLayer) {
    // Switch to log legend
    if (eventLayer.name === 'Log') {
        this.removeControl(legend_lin);
        legend_log.addTo(this);
    } else { // Or switch to linear legend
        this.removeControl(legend_log);
        legend_lin.addTo(this);
    }
});
