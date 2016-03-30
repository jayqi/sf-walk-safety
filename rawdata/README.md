A stored .csv file with the ["SFPD Incidents - from 1 January 2003"](https://data.sfgov.org/Public-Safety/SFPD-Incidents-from-1-January-2003/tmnf-yvry) dataset from the SF OpenData portal. Run the shell script to download the file using `curl`.  

Make the script executable if necessary:  

    chmod +x downloaddata.sh  

Execute the script:  

    sh download-data.sh

The file will be downloaded to `SFPD_Incidents_-_from_1_January_2003.csv`

The time of download will be saved to `lastdownloaded.txt`
