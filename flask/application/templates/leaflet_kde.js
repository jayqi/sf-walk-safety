L.mapbox.accessToken = 'pk.eyJ1IjoianlxaSIsImEiOiJjaW01ZG11MjcwMWl0dGttM2R2c2JvbThiIn0.eE6Xt0dMIl7Y2tOT8e6dyQ';
var map = L.mapbox.map('map', 'mapbox.light',{
    minZoom:12,
    maxZoom:18
})
    .setView([37.7680, -122.4367], 12);

{% if '/thefts/' in request.path %}
    var kde = L.mapbox.tileLayer('jyqi.3ghnstl4').addTo(map);
{% elif '/robberies/' in request.path %}
    var kde = L.mapbox.tileLayer('jyqi.d32de2yt').addTo(map);
{% endif %}
kde.setOpacity(0.66)
