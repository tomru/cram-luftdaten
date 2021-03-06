#!/usr/bin/env python3

""" Converts CSV exports from https://www.madavi.de/sensor/csvfiles.php to InfluxDB LineProtocol

    Note: timestamps are in seconds, therefore precision "s" needs to be set
    when writing, see https://docs.influxdata.com/influxdb/v1.2/tools/api/#write

Settings:

    Please set
    * SENSOR_ID
    * INFLUXDB_DATABASE
    in your environment

CSV file spec:

    Semiconlos are used as delimiters. First line are the header columns.
    Generally the column name is used as a DB field name.
    
    The format before 2018-10-01 is not supported by this script and should
    be manually converted.

    | DB Field name      | DB field | CSV Column         | CSV Format
    |--------------------|----------|--------------------|--------------------------
    | none               | time     | Time               | 2017/05/19 00:00:11 (UTC)
    | ?                  | ?        | durP1              |
    | ?                  | ?        | ratioP1            |
    | ?                  | ?        | P1                 |
    | ?                  | ?        | durP2              |
    | ?                  | ?        | ratioP2            |
    | ?                  | ?        | P2                 |
    | SDS_P1             | field    | SDS_P1             | 10.36
    | SDS_P2             | field    | SDS_P2             | 9.50
    | PMS_P1             | field    | PMS_P1             |
    | PMS_P2             | field    | PMS_P2             |
    | temperature        | field    | Temp               | 16.00
    | humidity           | field    | Humidity           | 79.00
    | BMP_temperature    | field    | BMP_temperature    |
    | BMP_pressure       | field    | BMP_pressure       |
    | BME280_temperature | field    | BME280_temperature |
    | BME280_humidity    | field    | BME280_humidity    |
    | BME280_pressure    | field    | BME280_pressure    |
    | samples            | field    | Samples            | 828799
    | min_micro          | field    | Min_cycle          | 172
    | max_micro          | field    | Max_cycle          | 25198
    | signal             | field    | Signal             | -91
    | node               | tag      | N/A filename?      | e.g. esp8266-16229960

"""

import os
import sys
import csv
from datetime import datetime, timedelta


def get_timestamp(timestr):
    """Converts CSV time value to a UTC timestamp in seconds"""
    naive_dt = datetime.strptime(timestr, "%Y/%m/%d %H:%M:%S")
    utc = (naive_dt - datetime(1970, 1, 1)) / timedelta(seconds=1)
    return int(utc)


SENSOR_ID = os.environ.get("SENSOR_ID", "16229960")
DATABASE = os.environ.get("INFLUXDB_DATABASE", "sensors")

NODE = "esp8266-" + SENSOR_ID

NAME_MAP = {
    "Humidity": "humidity",
    "Max_cycle": "max_micro",
    "Samples": "samples",
    "Min_cycle": "min_micro",
    "Signal": "signal",
    "Temp": "temperature",
}

READER = csv.DictReader(sys.stdin, delimiter=";")
for row in READER:
    # error out on legacy format until it's clear what that format is
    if row["Time"] == "time":
        raise Exception(
            "Looks like a legacy format not supported yet. Send the file to the author please."
        )

    # catch multiple column headers
    if row["Time"] == "Time":
        continue

    measurements = []
    for header, value in row.items():
        if header == "Time" or not value:
            continue
        measurements.append("{0}={1}".format(NAME_MAP.get(header, header), value))

    values = {
        "database": DATABASE,
        "node": NODE,
        "measurements": ",".join(measurements),
        "time": get_timestamp(row["Time"]),
    }

    print("{database},node={node} {measurements} {time}".format(**values))
