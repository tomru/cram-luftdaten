#!/usr/bin/env python3
#
# Converts CSV exports from https://www.madavi.de/sensor/csvfiles.php to
# InfluxDB LineProtocol https://docs.influxdata.com/influxdb/v1.2/write_protocols/line_protocol_reference/
#
# Note: timestamps are in seconds, therefore precision "s" needs to be set
# when writing, see https://docs.influxdata.com/influxdb/v1.2/tools/api/#write
#
# Settings:
#
# Please set
#   * SENSOR_ID
#   * INFLUXDB_DATABASE
# in your environment

# CSV file specs
#
# | DB Field    | DB field | CSV Column            | CSV Format
# |-------------|----------|-----------------------|--------------------------
# | time        | time     | 1  Time               | 2017/05/19 00:00:11 (UTC)
# |             |          | 2  durP1              |
# |             |          | 3  ratioP1            |
# |             |          | 4  P1                 |
# |             |          | 5  durP2              |
# |             |          | 6  ratioP2            |
# |             |          | 7  P2                 |
# | SDS_P1      | field    | 8  SDS_P1             | 10.36
# | SDS_P2      | field    | 9  SDS_P2             | 9.50
# | temperature | field    | 10 Temp               | 16.00
# | humidity    | field    | 11 Humidity           | 79.00
# |             |          | 12 BMP_temperature    |
# |             |          | 13 BMP_pressure       |
# |             |          | 14 BME280_temperature |
# |             |          | 15 BME280_humidity    |
# |             |          | 16 BME280_pressure    |
# | samples     | field    | 17 Samples            | 828799
# | min_micro   | field    | 18 Min_cycle          | 172
# | max_micro   | field    | 19 Max_cycle          | 25198
# |             |          | 20 Signal             | -91
# | node        | tag      | -- --                 | e.g. esp8266-16229960
#

import os
import sys
import csv
from datetime import datetime, timedelta

def getTimestamp(timestr):
    naiveDt = datetime.strptime(timestr, '%Y/%m/%d %H:%M:%S');
    utcTimestamp = (naiveDt - datetime(1970, 1, 1)) / timedelta(seconds=1)
    return int(utcTimestamp)

sensor_id = os.environ.get('SENSOR_ID', '16229960')
database = os.environ.get('INFLUXDB_DATABASE', 'feinstaub')

node = 'esp8266-' + sensor_id
outline = '{database},node={node} SDS_P1={sds_p1},SDS_P2={sds_p2},humidity={humidity},min_micro={min_micro},max_micro={max_micro},samples={samples},temperature={temperature} {timestamp}'

reader = csv.reader(sys.stdin, delimiter=';')
for row in reader:
    if (row[0] == 'Time'):
        continue

    values = {}
    values['database'] = database
    values['node'] = node
    values['timestamp'] = getTimestamp(row[0])
    values['sds_p1'] = row[7]
    values['sds_p2'] = row[8]
    values['temperature'] = row[9]
    values['humidity'] = row[10]
    values['samples'] = row[16]
    values['min_micro'] = row[17]
    values['max_micro'] = row[18]

    print(outline.format(**values))
