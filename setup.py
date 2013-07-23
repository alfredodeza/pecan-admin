# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = 'pecan-admin',
    version = '0.0.1',
    description = 'An admin interface for the Pecan framework',
    author = 'Alfredo Deza',
    author_email = 'alfredo [at] deza.pe',
    install_requires = [
        'pecan', 
        'sqlalchemy<=0.9', 
        'Beaker==1.6.4',
        'WebHelpers==1.3',
        ],
    zip_safe = False,
    include_package_data = True,
    packages = find_packages(exclude=['ez_setup']),
)
