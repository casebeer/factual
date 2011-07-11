import logging
import httplib2
try:
	import simplejson as json
except ImportError:
	import json

import requests
import tables

class Session(object):
	'''
	Main entry point to access the Factual "Server" API. 

	Session instances hold API level configuration; specifically, the api_key and api_base URL to use.

	Session instances also create read, input, rate, duplicates, or schema request objects that
	can be used to build and run requests against the Facutal API. See the requests module for 
	details on customizing API requests. 

	Session instances should be the *only* way you create request objects. 

	Examples:

		s = Session(api_key="deadbeef")
		records = s.read(tables.USPOI).search("coffee").run().records()
		s.rate(tables.USLocalPlaypen).subject_key("foobar").rate(1).run()
	
	Note that "Session" is meant loosely in the "login session" sense, *not* the "transaction" sense.
	'''
	_url_pat = "%(api_base)s/tables/%(table_id)s/%(action)s?api_key=%(api_key)s&%(query)s"
	def __init__(self, api_key=None, api_base="http://api.factual.com/v2"):
		'''Provide an api_key to use with the Factual API.'''
		self.api_key = api_key
		self.api_base = api_base
	def run(self, request):
		url = self._url_pat % {
				'api_base': self.api_base,
				'table_id': request.table.id,
				'action':   request.action,
				'api_key':  self.api_key,
				'query':    request.get_query()
			}
		logging.debug(url)
		h = httplib2.Http()
		http_response, http_body = h.request(url)
		# todo: timing and other metrics
		meta = {}
		response = request.make_response(json.loads(http_body), meta=meta)
		return response
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

