#!/usr/bin/env bash
#
# TODO: explain usage

set -e

HOST=${INFLUXDB_HOST:-localhost}
PORT=${INFLUXDB_PORT:-8086}
DATABASE=${INFLUXDB_DATABASE:-feinstaub}

PRECISION=s

SRC_FILE=${1:-/dev/stdin}

curl --include -X POST \
    "http://${HOST}:${PORT}/write?db=${DATABASE}&precision=${PRECISION}" \
    --data-binary @${SRC_FILE}
