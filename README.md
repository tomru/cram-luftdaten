# Cram Luftdaten

Helpers to write CSV files from https://www.madavi.de/sensor/csvfiles.php to
your InfluxDb.

You can use this to fill up your local InfluxDB with previous data or fill data gaps in your influxdb.

# How does it work

* get the relevant CSVs from https://www.madavi.de/sensor/csvfiles.php 
  **Only data after 2018-10-01 is supported, previous format not yet. PRs welcome**
* delete all lines that you already have in your DB (you must keep the csv header line)
* export settings as environment vars in case they differ from the defaults
  (INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_DATABASE, SENSOR_ID)
* run `cat file1.csv [ file2.csv ...] | ./to_line_protocol.py | ./to_influx_db.sh`

I should advise you to backup the DB first :stuck_out_tongue:
