#!/bin/sh

URL="https://data.sfgov.org/api/views/tmnf-yvry/rows.csv?accessType=DOWNLOAD"
FILENAME="SFPD_Incidents_-_from_1_January_2003.csv"

curl -o $FILENAME $URL

echo "$(date)" > last-downloaded.txt
