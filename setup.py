#!/usr/bin/env python

from setuptools import setup, find_packages

required_modules = [
	"simplejson",
	"httplib2",
	"unidecode",
	"oauth2"
	]

with open("README.md", "rb") as f:
	readme = f.read()

setup(
	name="factual",
	version="0.1.2",
	description="Wrapper for the Factual HTTP API.",
	author="Christopher H. Casebeer",
	author_email="",
	url="https://github.com/casebeer/factual",

	packages=find_packages(exclude='tests'),
	install_requires=required_modules,

	tests_require=["nose"],
	test_suite="nose.collector",

	long_description=readme,
	classifiers=[
		"License :: OSI Approved :: BSD License",
		"Intended Audience :: Developers",
	]
)

