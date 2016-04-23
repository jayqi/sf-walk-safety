<!-- Leaflet Map -->

L.mapbox.accessToken = 'pk.eyJ1IjoianlxaSIsImEiOiJjaW01ZG11MjcwMWl0dGttM2R2c2JvbThiIn0.eE6Xt0dMIl7Y2tOT8e6dyQ';
var map = L.mapbox.map('map', 'mapbox.light')
.setView([37.7680, -122.4367], 12);

map.scrollWheelZoom.disable();

var heat = L.heatLayer({{ mapdata | safe }}, {minOpacity: 0.66, radius: 10 ,blur: 3, gradient: {0.0: 'blue', 1.0: 'red'}}).addTo(map);
