#!/usr/bin/env python
# encoding: utf-8

import setuptools


setuptools.setup(
    name='py-datove-schranky-bin',
    version='0.1',
    description='',
    license='BSD',
    url='https://github.com/vencax/PyDatoveSchrankyBinarky',
    author='vencax',
    author_email='vencax@vxk.cz',
    packages=setuptools.find_packages(),
    platforms=['Unix', 'Windows', 'MacOS X'],
    data_files=[
        ('share/pydatoveschranky', ['README.txt']),
        ('bin', ['sendmessage.py']),
    ],
    requires=['pyOpenSSL (>=0.9)', 'pyasn1 (>=0.0.13)'],
    install_requires=['pyOpenSSL>=0.9', 'pyasn1>=0.0.13'],
    keywords='datove,schranky',
    include_package_data=True,
)
