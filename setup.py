#!/usr/bin/env python

from setuptools import setup, find_packages
import versioneer

requires = open('requirements.txt').read().strip().split('\n')

setup(
    name='intake-excel',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Intake Excel plugin',
    url='https://github.com/franprix/intake-excel',
    maintainer='Guillaume Ansanay-Alex',
    maintainer_email='gansanay@franprix.fr',
    license='MIT',
    py_modules=['intake_excel'],
    packages=['intake_excel'],
    # package_data={'': ['*.pcap', '*.yml', '*.html']},
    include_package_data=True,
    install_requires=requires,
    long_description=open('README.md').read(),
    zip_safe=False,
)