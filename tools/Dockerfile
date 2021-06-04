FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y build-essential libffi-dev git pkg-config python python3 && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/micropython/micropython.git && \
    cd micropython && \
    git checkout v1.15 && \
    git submodule update --init && \
    cd mpy-cross && \
    make && \
    cd .. && \
    cd ports/unix && \
    make axtls && \
    make && \
    make test && \
    make install && \
    apt-get purge --auto-remove -y  build-essential libffi-dev git pkg-config python python3 && \
    cd ../../.. && \
    rm -rf micropython

CMD ["/usr/local/bin/micropython"]

