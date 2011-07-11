#!/usr/bin/env python
from setuptools import setup, find_packages

required_modules = [
	"simplejson",
	"httplib2",
	"urllib",
	"unidecode",
	]

setup(
	name="factual",
	version="0.0.1",
	description="",
	author="Christopher H. Casebeer",
	author_email="chc@plac.es",
	url="",
	packages=find_packages(exclude='tests'),
#	entry_points='''
#		[console_scripts]
#		factualshell = factual.cli.factualshell:main
#	''',
	install_requires=required_modules
	)

