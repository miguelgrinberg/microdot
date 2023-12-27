#!/bin/bash
# this script updates the micropython binary in the /bin directory that is
# used to run unit tests under GitHub Actions builds

DOCKER=${DOCKER:-docker}
VERSION=${1:-main}

$DOCKER build -f Dockerfile.circuitpython --build-arg VERSION=$VERSION -t circuitpython .
$DOCKER create -t --name dummy-circuitpython circuitpython
$DOCKER cp dummy-circuitpython:/usr/local/bin/micropython ../bin/circuitpython
$DOCKER rm dummy-circuitpython
