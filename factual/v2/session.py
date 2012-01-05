import logging
import httplib2
try:
	import simplejson as json
except ImportError:
	import json

import requests
import tables
import factual.common.session

class Session(factual.common.session.BaseSession):
	def read(self, table_type):
		'''Build a Read request on the provided Table type using this Session. See the requests module for details.'''
		return requests.Read(self, table_type())
	def input(self, table_type):
		'''Build an Input request on the provided Table type using this Session. See the requests module for details.'''
		return requests.Input(self, table_type())
	def rate(self, table_type):
		'''Build a Rate request on the provided Table type using this Session. See the requests module for details.'''
		return requests.Rate(self, table_type())
	def duplicates(self, table_type):
		'''Build a Duplicates request on the provided Table type using this Session. See the requests module for details.'''
		return requests.Duplicates(self, table_type())
	def schema(self, table_type):
		'''Build a Schema request on the provided Table type using this Session. See the requests module for details.'''
		return requests.Schema(self, table_type())

