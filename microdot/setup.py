"""
Microdot
--------

The impossibly small web framework for MicroPython.
"""
from setuptools import setup

setup(
    name='microdot',
    version="0.4.0",
    url='http://github.com/miguelgrinberg/microdot/',
    license='MIT',
    author='Miguel Grinberg',
    author_email='miguel.grinberg@gmail.com',
    description='The impossibly small web framework for MicroPython',
    long_description=__doc__,
    py_modules=['microdot'],
    platforms='any',
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
