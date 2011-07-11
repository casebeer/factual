#!/usr/bin/env python
from setuptools import setup, find_packages
from factual import APP_NAME, __version__, __author__

required_modules = [
	"simplejson",
	"httplib2",
	"unidecode",
	]

setup(
	name=APP_NAME,
	version=__version__,
	description="",
	author=__author__,
	author_email="",
	url="",
	packages=find_packages(exclude='tests'),
#	entry_points='''
#		[console_scripts]
#		factualshell = factual.cli.factualshell:main
#	''',
	install_requires=required_modules
	)

