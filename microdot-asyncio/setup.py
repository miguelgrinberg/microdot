"""
Microdot-AsyncIO
----------------

AsyncIO support for the Microdot web framework.
"""
from setuptools import setup

setup(
    name='microdot-asyncio',
    version="0.4.0",
    url='http://github.com/miguelgrinberg/microdot/',
    license='MIT',
    author='Miguel Grinberg',
    author_email='miguel.grinberg@gmail.com',
    description='AsyncIO support for the Microdot web framework',
    long_description=__doc__,
    py_modules=['microdot_asyncio'],
    platforms='any',
    install_requires=[
        'microdot',
        'micropython-uasyncio;implementation_name=="micropython"'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: MicroPython',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
