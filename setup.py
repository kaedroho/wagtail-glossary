#!/usr/bin/env python

import sys, os

from setuptools import setup, find_packages

# Hack to prevent "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when setup.py exits
# (see http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing
except ImportError:
    pass


setup(
    name="wagtail-glossary",
    version="0.1",
    description="Adds glossary management into Wagtail admin and search.",
    author="Karl Hobley",
    author_email="karl@kaed.uk",
    url="",
    packages=find_packages(),
    include_package_data=True,
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=["Django>=2.2,<3.2", "Wagtail>=2.10,<2.11"],
    extras_require={
        "testing": ["dj-database-url==0.5.0", "freezegun==0.3.15"],
    },
    zip_safe=False,
)
