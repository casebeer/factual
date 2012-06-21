import logging
import urllib
import unidecode
try:
	import simplejson as json
except ImportError:
	import json

import responses
import shared_filter_helpers
import util

class Request(object):
	response_type = responses.Response
	def __init__(self, session, table):
		self.session = session
		# instantiate the table class if we're passed a type rather than an instance (or a string)
		self.table = table() if isinstance(table, type) else table
	def run(self, async=False):
		'''
		Perform the Factual API HTTP request. 

		By default, process and return the API response wrapped in a
		FactualResponse object. 

		Pass `async = True` to perform the request asynchronously; in 
		async mode, `run` returns a function, get_response, that will 
		process and return the response when called. 
		
		Additionally, if the asynchttp module is available and async is
		True, the initial HTTP request will not block, and get_response
		will be returned immediately.  get_response function will block 
		when called if the HTTP requst is not yet complete. 
		'''
		return self.session.run(self, async)
	def make_response(self, *args, **kwargs):
		response = self.response_type(*args, **kwargs)
		return response
	def unparse_dict(self, d):
		return unidecode.unidecode(\
			json.dumps(d,ensure_ascii=False, \
					separators=(',',':')))
	def join_params(self, params, suppress_null=True):
		''' 
		Custom alternative to urllib.urlencode that keeps URL length
		down by not escaping certain special characters that Factual
		can tolerate unescaped. This is especially useful for the 
		JSON special chars {}[],:. 

		The full list of usually-escaped-but-ok-for-factual characters is:

		    / { } ' $ : , [ ]

		The API used to tolerate doublequotes, but this seems to have 
		changed. 

		suppress_null removes parametrs which are set to None.
		'''
		# ensure all params and values are properly urlencoded
		# since we may have numbers, etc. here, cast to unicode and encode back to utf-8
		return "&".join([
					("%s=%s" \
						% (
							urllib.quote_plus(unicode(k).encode('utf-8'), '/{}\'$:,[]'),
							urllib.quote_plus(unicode(v).encode('utf-8'), '/{}\'$:,[]')
						)
					) 
					for k,v 
					in params.iteritems()
					if not suppress_null or v != None
				])

				
	def get_query(self): util.abstract()
class WriteRequest(Request):
	pass
class Read(Request):
	'''
	Query object used to build Factual read requests. 

	Read objects should be created by calling read(<Table type>) on a Session object:
		s = Session()
		query = s.read("places")
	
	Creating a query object this way automatically binds it to the Session and Table.
	
	A Read query can be customized with filters and other paramters. Read objects'
	functions return the same Read object, making them chainable:
		query = s.read("places")
		query = query.filter({"name":"foobar"}).filter({"address":"123 Main St."})
	
	Once a query is ready, call run to get a Result object. Read queries return
	ReadResult objects which process the returned data rows into dicts:
		res = query.run()
		records = res.records()

	or, chained:
		records = s.read(tables.USPOI).filter({"name":"foobar"}).run().records()
	'''
	action = "read"
	response_type = responses.ReadResponse
	def __init__(self, session, table):
		Request.__init__(self, session, table)
		self._filters = {}
		self._count = 20
		self._page = 1
	def get_query(self):
		return self.join_params(self.get_params())
	def get_params(self):
		filters = dict([(k,v) for k,v in self._filters.iteritems() if v != None])

		params = {
			"filters": self.unparse_dict(filters) if filters != {} else None,
			"limit": self._count
		}

		offset = self._count * (self._page - 1)
		if offset > 0:
			params["offset"] = offset

		return params
	def count(self, count):
		'''Set the number of results to return per page. N.B. Factual caps this at 50.'''
		self._count = count 
		return self #chainable
	def page(self, page):
		'''
		Set the page to return. Factual caps the number of rows requestable, or page * count, 
		at 500.
		'''
		self._page = page
		return self
	
	def filter(self, filter):
		'''
		Add a filter to this Read request.

		The filter should be a dict containing a valid Factual filter tree.
		filter() can be called multiple times. Filter dict combination is handled
		with dict.update(), so subsequent conflicting keys will overwrite previous 
		values. 

		The helper functions in the filter_helpers module can be used to generate
		valid Facutal filter dicts.

		To remove a filter already applied, pass a dict containing the key to remove 
		with None as its value.

		Examples:
			- s.read(tables.USPOI).filter({"name":{"$bw":"foo"}})
			- Use filter_helpers:
				from filter_helpers import *
				s.read(tables.USPOI).filter(bw_("name", "foo"))
			- Set name and $search filters:
				s.read(tables.USPOI).filter({"name":"foobar"}).filter({"$search":"baz"})
			- Overwrite previous value; name:baz prevails
				s.read(tables.USPOI).filter({"name":"foobar"}).filter({"name":"baz"}) 
			- Remove previous filter:
				s.read(tables.USPOI).filter({"name":"foobar"}).filter({"name":None})

		'''
		self._filters.update(filter)
		return self # chainable
	def name(self, term):
		'''Convenience method to apply a {"name":...} filter'''
		return self.filter(shared_filter_helpers.eq_("name", term))
class Schema(Request):
	action = "schema"
	response_type = responses.SchemaResponse
	def get_query(self):
		# schema action takes no parameters
		return ""

