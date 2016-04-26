L.mapbox.accessToken = 'pk.eyJ1IjoianlxaSIsImEiOiJjaW01ZG11MjcwMWl0dGttM2R2c2JvbThiIn0.eE6Xt0dMIl7Y2tOT8e6dyQ';
var map = L.mapbox.map('map', 'mapbox.light',{
    minZoom:12,
    maxZoom:18
})
    .setView([37.7680, -122.4367], 12);

map.scrollWheelZoom.disable();


// Load log kde tiles and add to map
{% if '/thefts/' in request.path %}
    var kde_log = L.mapbox.tileLayer('jyqi.3ghnstl4').addTo(map);
{% elif '/robberies/' in request.path %}
    var kde_log = L.mapbox.tileLayer('jyqi.d32de2yt').addTo(map);
{% endif %}
kde_log.setOpacity(0.66)

// Load linear kde tiles
{% if '/thefts/' in request.path %}
    var kde_lin = L.mapbox.tileLayer('jyqi.66cjswal')
{% elif '/robberies/' in request.path %}
    var kde_lin = L.mapbox.tileLayer('jyqi.bcdd6b0w')
{% endif %}
kde_lin.setOpacity(0.66)

// Layer control
var kdes = {
    "Log": kde_log,
    "Linear": kde_lin
};
L.control.layers(kdes).addTo(map);


// Define log legend
var legend_log = L.control({position: 'bottomright'});
legend_log.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'mapinfo maplegend');
    div.innerHTML += 'Log color scale:' + '<br>' +
            '<i style="background: #ffffcc"></i> 0.0' + '<br>' +
            '<i style="background: #ffeda0"></i> 0.001' + '<br>' +
            '<i style="background: #fed976"></i> 0.0027' + '<br>' +
            '<i style="background: #feb24c"></i> 0.0072' + '<br>' +
            '<i style="background: #fd8d3c"></i> 0.019' + '<br>' +
            '<i style="background: #fc4e2a"></i> 0.052' + '<br>' +
            '<i style="background: #e31a1c"></i> 0.14' + '<br>' +
            '<i style="background: #bd0026"></i> 0.37' + '<br>' +
            '<i style="background: #800026"></i> 1.0';
    return div;
};



// Define linear legend
var legend_lin = L.control({position: 'bottomright'});
legend_lin.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'mapinfo maplegend');
    div.innerHTML += 'Linear color scale:' + '<br>' +
            '<i style="background: #ffffcc"></i> 0.0' + '<br>' +
            '<i style="background: #ffeda0"></i> 0.125' + '<br>' +
            '<i style="background: #fed976"></i> 0.25' + '<br>' +
            '<i style="background: #feb24c"></i> 0.375' + '<br>' +
            '<i style="background: #fd8d3c"></i> 0.5' + '<br>' +
            '<i style="background: #fc4e2a"></i> 0.625' + '<br>' +
            '<i style="background: #e31a1c"></i> 0.75' + '<br>' +
            '<i style="background: #bd0026"></i> 0.875' + '<br>' +
            '<i style="background: #800026"></i> 1.0';
    return div;
};



// Add it to map because it's default
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
