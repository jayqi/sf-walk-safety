<!-- Leaflet Map -->

L.mapbox.accessToken = 'pk.eyJ1IjoianlxaSIsImEiOiJjaW01ZG11MjcwMWl0dGttM2R2c2JvbThiIn0.eE6Xt0dMIl7Y2tOT8e6dyQ';
var map = L.mapbox.map('map', 'mapbox.streets')
.setView([37.7833, -122.4167], 13);




var geoJsonLayer = L.geoJson(dataset, {
   onEachFeature: function(feature, layer) {
      layer.bindPopup(
          'Date: ' + feature.properties.Date + '<br />' +
          'Time: ' + feature.properties.Time + '<br />' +
          'Description: ' + feature.properties.Descript);
   }
})

var markers_cluster = new L.MarkerClusterGroup({
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
map.addLayer(markers_cluster)
