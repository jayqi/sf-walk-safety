<!-- Leaflet Map -->

L.mapbox.accessToken = 'pk.eyJ1IjoianlxaSIsImEiOiJjaW01ZG11MjcwMWl0dGttM2R2c2JvbThiIn0.eE6Xt0dMIl7Y2tOT8e6dyQ';
var map = L.mapbox.map('map', 'mapbox.streets', {
    minZoom:12
})
    .setView([37.7680, -122.4367], 12);

map.scrollWheelZoom.disable();

function build_popup(feature) {
    var popuptext = 'Date: ' + feature.properties.date + '<br />' +
    'Time: ' + feature.properties.time + '<br />' +
    'Day of Week: ' + feature.properties.dayofweek + '<br />'
    {% if ('/thefts/' in request.path) or ('/robberies/' in request.path) %}
    +
    'Location: ' + feature.properties.address + '<br />' +
    'Description: ' + feature.properties.descript
    {% elif '/trafficcollisions/' in request.path %}
    +
    'Location: ' + feature.properties.location + '<br />' +
    '<br />' +
    'Primary Collision Factor: ' + feature.properties.PRIMARY_COLLISION_FACTOR + '<br />' +
    'Weather: ' + feature.properties.WEATHER + '<br />' +
    'Road surface: ' + feature.properties.ROAD_SURFACE + '<br />' +
    'Road condition: ' + feature.properties.ROAD_COND + '<br />' +
    'Lighting: ' + feature.properties.LIGHTING + '<br />' +
    ((feature.properties.HIT_AND_RUN != 'No') ? feature.properties.HIT_AND_RUN + '<br />': '') +
    ((feature.properties.ALCOHOL_INVOLVED) ? 'Alcohol Involved' + '<br />': '') +
    '<br />' +
    'Pedestrian action: ' + feature.properties.PED_ACTION +
    ((feature.properties.COUNT_PED_INJURED > 0) ? '<br /> Pedestrians injured: ' + feature.properties.COUNT_PED_INJURED : '') +
    ((feature.properties.COUNT_PED_KILLED > 0) ? '<br /> Pedestrians injured: ' + feature.properties.COUNT_PED_KILLED : '') +
    ''
    {% endif %}
    ;
    return popuptext;
}

var geoJsonLayer = L.geoJson(data, {
   onEachFeature: function(feature, layer) {
      layer.bindPopup(build_popup(feature));}
});

var markers_cluster = new L.MarkerClusterGroup({
    spiderfyOnMaxZoom: true,
    spiderLegPolylineOptions: { weight: 3.0, color: '#000', opacity: 0.66 },
    iconCreateFunction: function(cluster){
        var childCount = cluster.getChildCount();
        var c = ' marker-cluster-';
        if (childCount < 100) {
            c += 'small';
        } else if (childCount < 1000) {
            c += 'medium';
        } else {
            c += 'large';
        }
        return new L.DivIcon({ html: '<div><span>' + childCount + '</span></div>', className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) });
    }
});

markers_cluster.addLayer(geoJsonLayer);
map.addLayer(markers_cluster);
