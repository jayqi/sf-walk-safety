L.mapbox.accessToken = 'pk.eyJ1IjoianlxaSIsImEiOiJjaW01ZG11MjcwMWl0dGttM2R2c2JvbThiIn0.eE6Xt0dMIl7Y2tOT8e6dyQ';

var splitmap1 = L.mapbox.map('splitmap1', 'mapbox.light',{
        minZoom:12,
        maxZoom:18
    })
    .setView([37.7680, -122.4367], 12);

var splitmap2 = L.mapbox.map('splitmap2', 'mapbox.light',{
        minZoom:12,
        maxZoom:18
    })
    .setView([37.7680, -122.4367], 12);


splitmap1.scrollWheelZoom.disable();
splitmap2.scrollWheelZoom.disable();

var kde_thefts = L.mapbox.tileLayer('jyqi.3nj276s8').addTo(splitmap1);
kde_thefts.setOpacity(0.66)

var kde_robberies = L.mapbox.tileLayer('jyqi.32dcovup').addTo(splitmap2);
kde_robberies.setOpacity(0.66)

// when either map finishes moving, trigger an update on the other one.
splitmap1.on('moveend', follow).on('zoomend', follow);
splitmap2.on('moveend', follow).on('zoomend', follow);

// quiet is a cheap and dirty way of avoiding a problem in which one map
// syncing to another leads to the other map syncing to it, and so on
// ad infinitum. this says that while we are calling sync, do not try to
// loop again and sync other maps
var quiet = false;
function follow(e) {
    if (quiet) return;
    quiet = true;
    if (e.target === splitmap1) sync(splitmap2, e);
    if (e.target === splitmap2) sync(splitmap1, e);
    quiet = false;
}

// sync simply steals the settings from the moved map (e.target)
// and applies them to the other map.
function sync(map, e) {
    map.setView(e.target.getCenter(), e.target.getZoom(), {
        animate: false,
        reset: true
    });
}





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


// Add legend to map
var legendon = false

L.easyButton( '<strong>L</strong>', function(){
    if (legendon) {
        legend_log.removeFrom(splitmap2);
        legendon = false;
    } else {
        legend_log.addTo(splitmap2);
        legendon = true;
    }
}).addTo(splitmap2);
