"""
Microdot
--------

Impossibly small web framework for MicroPython.
"""
from setuptools import setup

setup(
    name='microdot',
    version='0.1.1',
    url='http://github.com/miguelgrinberg/microdot/',
    license='MIT',
    author='Miguel Grinberg',
    author_email='miguel.grinberg@gmail.com',
    description='Impossibly small web framework for MicroPython',
    long_description=__doc__,
    py_modules=['microdot'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    tests_require=[
        'coverage'
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
