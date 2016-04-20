// Date filter
$('#daterange').daterangepicker({
    "showDropdowns": true,
    "autoApply": true,
    "ranges": {
        "All Data (2003-2015)": [
            "2003-01-01",
            "2015-12-31"
        ],
        "Last Five Years (2011-2015)": [
            "2011-01-01",
            "2015-12-31"
        ],
        "Last Year (2015)": [
            "2015-01-01",
            "2015-12-31"
        ],
    },
    "linkedCalendars": false,
    "startDate": "{{ filtersdisplay['startDate'] }}",
    "endDate": "{{ filtersdisplay['endDate'] }}",
    "minDate": "01/01/2003",
    "maxDate": "03/01/2016"
}, function(start, end, label) {
  console.log("New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')");
});

// Time filter
$('#startTime').timepicker({
    'timeFormat' : 'H:i',
    'show2400' : true,
    'step' : 60
});
$('#endTime').timepicker({
    'timeFormat' : 'H:i',
    'show2400' : true,
    'step' : 60
});

// Temperature filters (sliders)
$("#hiTemp").slider({
    tooltip: 'always'
});
$("#loTemp").slider({
    tooltip: 'always'
});
