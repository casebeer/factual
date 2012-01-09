import logging
import httplib2
try:
	import simplejson as json
except ImportError:
	import json

class BaseSession(object):
	'''
	Main entry point to access the Factual "Server" API. 

	Session instances hold API level configuration; specifically, the api_key and api_base URL to use.

	Session instances also create read, input, rate, duplicates, or schema request objects that
	can be used to build and run requests against the Facutal API. See the requests module for 
	details on customizing API requests. 

	Session instances should be the *only* way you create request objects. 

	Examples:

		s = Session(api_key="deadbeef")
		records = s.read("places").search("coffee").run().records()
	
	Note that "Session" is meant loosely in the "login session" sense, *not* the "transaction" sense.
	'''
	_url_pat = "%(api_base)s/tables/%(table_id)s/%(action)s?api_key=%(api_key)s&%(query)s"
	def __init__(self, api_key=None, api_base="http://api.factual.com/v2"):
		'''Provide an api_key to use with the Factual API.'''
		self.api_key = api_key
		self.api_base = api_base
	def get_url(self, request):
		return self._url_pat % {
				'api_base': self.api_base,
				'table_id': request.table,
				'action':   request.action,
				'api_key':  self.api_key,
				'query':    request.get_query()
			}
	def get_headers(self, request):
		return {}
	def run(self, request):
		url = self.get_url(request)
		headers = self.get_headers(request)

		logging.debug(url)
		logging.debug(headers)
		h = httplib2.Http()
		http_response, http_body = h.request(url, headers=headers)
		# todo: timing and other metrics
		meta = {}
		response = request.make_response(json.loads(http_body), meta=meta)
		return response

