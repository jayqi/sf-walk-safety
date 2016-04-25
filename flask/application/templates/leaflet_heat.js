<!-- Leaflet Map -->

L.mapbox.accessToken = 'pk.eyJ1IjoianlxaSIsImEiOiJjaW01ZG11MjcwMWl0dGttM2R2c2JvbThiIn0.eE6Xt0dMIl7Y2tOT8e6dyQ';
var map = L.mapbox.map('map', 'mapbox.light', {
        minZoom:12,
        maxZoom:14
    })
    .setView([37.7680, -122.4367], 13);

map.scrollWheelZoom.disable();

var heat = L.heatLayer(
    {{ mapdata | safe }},
    {
        minOpacity: 1,
        radius: 3 ,
        blur: 5,
    }).addTo(map);
