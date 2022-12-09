#!/bin/bash
# this script updates the micropython binary in the /bin directory that is
# used to run unit tests under GitHub Actions builds

DOCKER=${DOCKER:-docker}

$DOCKER build -t micropython .
$DOCKER create -it --name dummy-micropython micropython
$DOCKER cp dummy-micropython:/usr/local/bin/micropython ../bin/micropython
$DOCKER rm dummy-micropython
