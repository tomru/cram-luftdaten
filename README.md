# Write Luftdaten CSV to a InfluxDB

Helpers to write CSV files from https://www.madavi.de/sensor/csvfiles.php to
your InfluxDb.

# How does it work

* get the relevant CSVs from https://www.madavi.de/sensor/csvfiles.php (dates
  are in UTC!)
* delete all lines that you already have in your DB (you can keep the csv header line)
* export settings as environment vars in case they differ from the defaults
  (INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_DATABASE, SENSOR_ID)
* run `cat <file1.csv> [file2.csv...] | ./toLineProtocol.py | ./toInfluxDb.sh`

I should advise you to backup the DB first :stuck_out_tongue:
