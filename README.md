# Write Luftdaten CSV to a InfluxDB

Helpers to write CSV files from https://www.madavi.de/sensor/csvfiles.php to
your InfluxDb.

# How does it work

* get the relevant CSVs from https://www.madavi.de/sensor/csvfiles.php
* delete all lines that you already have in your DB (keep the header)
* export settings as environment vars in case they differ from the defaults
  (INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_DATABASE, SENSOR_ID)
* run `cat <csv.file> | ./toLineProtocol.sh | ./toInfluxDb.sh`

I should advise you to backup the DB first :stuck_out_tongue:
