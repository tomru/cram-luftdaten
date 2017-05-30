#!/usr/bin/env bash
#
# Converts CSV exports from https://www.madavi.de/sensor/csvfiles.php to
# InfluxDB LineProtocol https://docs.influxdata.com/influxdb/v1.2/write_protocols/line_protocol_reference/
#
# Note: timestamps are in seconds, therefore precision "s" needs to be set
# when writing, see https://docs.influxdata.com/influxdb/v1.2/tools/api/#write

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
# TODO:
#   - using "date" to parse the UTC date for each line is super slow, but
#     works. There must be something better out there.

set -e

SRC_FILE=${1:-/dev/stdin}

DATABASE=${INFLUXDB_DATABASE:-feinstaub}
SENSOR_ID=${SENSOR_ID:-16229960}

NODE=esp8266-$SENSOR_ID

STRIP_CSV_HEADERS="tail -n +2"

cat $SRC_FILE                                                   \
    | $STRIP_CSV_HEADERS                                        \
    | gawk -v db="$DATABASE" -v node="$NODE"                    \
        'BEGIN { FS = ";" } ;                                   \
        {   convertDate = "date -u --date=\""$1"\" +%s";        \
            convertDate| getline timestamp;                     \
            close(convertDate);                                 \
            print db",node="node" SDS_P1="$8",SDS_P2="$9",humidity="$11",min_micro="$18",max_micro="$19",samples="$17",temperature="$10" "timestamp }'

