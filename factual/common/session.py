import logging
try:
	import asynchttp as http
except ImportError:
	import httplib2 as http

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
	def get_headers(self, request, defaults={}):
		return {}.update(defaults)
	def run(self, request, async=False):
		url = self.get_url(request)
		headers = self.get_headers(request)

		logging.debug(url)
		logging.debug(headers)

		h = http.Http()
		http_response, http_body = h.request(url, headers=headers)

		def get_response():
			'''
			Process and return the HTTP response from Factual.

			Performs the post-request processing needed to handle a Factual 
			response. Broken into a separate function so the post processing
			can be deferred, e.g. for use with asynchttp in place of
			httplib2. 

			When the asynchttp module is installed, this call will block
			if the HTTP request to Factual is not yet complete. 
			'''
			# todo: timing and other metrics
			meta = {}
			response = request.make_response(json.loads(str(http_body)), meta=meta)
			return response

		if async:
			return get_response
		else:
			return get_response()

