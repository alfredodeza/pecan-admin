# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = 'pecan-admin',
    version = '0.0.1',
    description = 'An admin interface for the Pecan framework',
    author = 'Alfredo Deza',
    author_email = 'alfredo [at] deza.pe',
    install_requires = [
        "Mako",
        "SQLAlchemy",
        "WTForms",
        "WebHelpers",
        "WebOb",
        "WebTest",
        "pecan",
        "pecan-wtforms",
        "simplegeneric",
        "wsgiref",
        "beaker",
    ],
    zip_safe = False,
    include_package_data = True,
    packages = find_packages(exclude=['ez_setup']),
    entry_points="""
        [pecan.command]
        admin=pecan_admin.commands.admin:AdminCommand
        """
)
