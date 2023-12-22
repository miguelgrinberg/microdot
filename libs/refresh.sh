#!/bin/bash
# this script downloads updated versions of all the MicroPython libraries

cd micropython
curl https://codeload.github.com/micropython/micropython/tar.gz/master | tar -xz --strip=2 micropython-master/extmod/asyncio
curl https://raw.githubusercontent.com/micropython/micropython-lib/master/python-stdlib/datetime/datetime.py > datetime.py
curl https://raw.githubusercontent.com/micropython/micropython-lib/d8e163bb5f3ef45e71e145c27bc4f207beaad70f/unix-ffi/ffilib/ffilib.py > ffilib.py
curl https://raw.githubusercontent.com/micropython/micropython-lib/master/python-stdlib/hmac/hmac.py > hmac.py
curl https://raw.githubusercontent.com/micropython/micropython-lib/master/python-stdlib/time/time.py > time.py
curl https://raw.githubusercontent.com/micropython/micropython-lib/master/python-stdlib/unittest/unittest/__init__.py > unittest.py
cd ../common
curl https://raw.githubusercontent.com/pfalcon/utemplate/master/README.md > utemplate/README.md
curl https://codeload.github.com/pfalcon/utemplate/tar.gz/master | tar -xz --strip=1 utemplate-master/utemplate
cd ..
