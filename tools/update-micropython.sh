# this script updates the micropython binary in the /bin directory that is
# used to run unit tests under GitHub Actions builds
docker build -t micropython .
docker create -it --name dummy-micropython micropython
docker cp dummy-micropython:/usr/local/bin/micropython ../bin/micropython
docker rm dummy-micropython
