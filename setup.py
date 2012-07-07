#!/usr/bin/env python

from setuptools import setup, find_packages
import sys
import subprocess

required_modules = [
	"simplejson",
	"httplib2",
	"unidecode",
	"oauth2"
	]

readme = ""
try:
	with open("README.md", "rb") as f:
		readme = f.read()

	# avoid ReST at all costs, but make sure we have it for PyPi
	proc = subprocess.Popen(
		["pandoc", "-fmarkdown", "-trst", "README.md"], 
		stdout=subprocess.PIPE
	)
	readme = proc.stdout.read()
except:
	if len(sys.argv) >=2:
		for command in ["register", "upload"]:
			if command in sys.argv[1:]:
				raise Exception("Unable to convert Markdown README to ReST for upload to PyPi. Do you have pandoc installed?")

setup(
	name="factual",
	version="0.1.3",
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

