#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

required_modules = [
	"simplejson",
	"httplib2",
	"unidecode",
	"oauth2"
	]

setup(
	name="factual",
	version="0.1.0",
	description="",
	author="Christopher H. Casebeer",
	author_email="",
	url="",
	packages=find_packages(exclude='tests'),
#	entry_points='''
#		[console_scripts]
#		factualshell = factual.cli.factualshell:main
#	''',
	install_requires=required_modules
	)

