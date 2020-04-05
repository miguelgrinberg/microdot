# microdot
[![Build Status](https://travis-ci.org/miguelgrinberg/microdot.svg?branch=master)](https://travis-ci.org/miguelgrinberg/microdot)

A minimalistic Python web framework for microcontrollers inspired by Flask

## Installation

Installation can be done directly from the microcontroller using the `upip` library.

```
>>> import upip
>>> upip.install(["microdot", "microdot-asyncio"])
```

Or, it can be downloaded on the host machine, and transferred to the device.

```
# Download the dependencies to the `lib` directory
micropython -m upip install -p lib microdot microdot-asyncio

# Transfer the `lib` directory to the microcontroller
ampy -p $PORT put lib
```

## Documentation

Coming soon!
