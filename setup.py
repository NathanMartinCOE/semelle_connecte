# -*- coding: utf-8 -*-
from setuptools import setup,find_packages
import os,sys
import logging

developMode = False
if len(sys.argv) >= 2:
    if sys.argv[1] == "develop": developMode = True
if developMode:
    logging.warning("You have sleected a developer model ( local install)")


VERSION ="0.0.1"


#------------------------- INSTALL--------------------------------------------
setup(name = 'semelle_connecte',
    version = VERSION,
    author = 'Nathan Martin',
    author_email = 'nathanmartin.coe@outlook.fr',
    description = "package for processing with sole",
    long_description= "",
    url = '',
    keywords = 'semelle_connecte',
    packages=find_packages(),
	include_package_data=True,
    license='',
	#install_requires = reqs,
    classifiers=['Programming Language :: Python',
                 'Programming Language :: Python :: 3.7',
                 'Operating System :: Microsoft :: Windows',
                 'Natural Language :: English'],
    )
