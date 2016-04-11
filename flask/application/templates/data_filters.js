// Date filter
$('#datefilter').daterangepicker({
    "showDropdowns": true,
    "autoApply": true,
    "ranges": {
        "Today": [
            "2016-04-10T23:17:55.572Z",
            "2016-04-10T23:17:55.572Z"
        ],
        "Yesterday": [
            "2016-04-09T23:17:55.572Z",
            "2016-04-09T23:17:55.572Z"
        ],
        "Last 7 Days": [
            "2016-04-04T23:17:55.572Z",
            "2016-04-10T23:17:55.572Z"
        ],
        "Last 30 Days": [
            "2016-03-13T00:17:55.572Z",
            "2016-04-10T23:17:55.572Z"
        ],
        "This Month": [
            "2016-04-01T07:00:00.000Z",
            "2016-05-01T06:59:59.999Z"
        ],
        "Last Month": [
            "2016-03-01T08:00:00.000Z",
            "2016-04-01T06:59:59.999Z"
        ]
    },
    "linkedCalendars": false,
    "startDate": "01/01/2003",
    "endDate": "03/01/2016",
    "minDate": "01/01/2003",
    "maxDate": "03/01/2016"
}, function(start, end, label) {
  console.log("New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')");
});

// Time filter
$('#startTime').timepicker();
$('#endTime').timepicker();

// Temperature filters (sliders)
$("#hiTemp").slider({
    tooltip: 'always'
});
$("#loTemp").slider({
    tooltip: 'always'
});
