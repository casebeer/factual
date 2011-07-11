import logging
import urllib
import unidecode
try:
	import simplejson as json
except ImportError:
	import json

import responses
import filter_helpers
import util

class Request(object):
	response_type = responses.Response
	def __init__(self, session, table):
		self.session = session
		self.table = table
	def run(self):
		return self.session.run(self)
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
		down by not unnecessarily escaping JSON special chars {}[],:"'

		suppress_null removes parametrs which are set to None.
		'''
		# ensure all params and values are properly urlencoded
		# since we may have numbers, etc. here, cast to unicode and encode back to utf-8
		return "&".join([
					("%s=%s" \
						% (
							urllib.quote_plus(unicode(k).encode('utf-8'), '/{}"\'$:,[]'),
							urllib.quote_plus(unicode(v).encode('utf-8'), '/{}"\'$:,[]')
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
		query = s.read(tables.USPOI)
	
	Creating a query object this way automatically binds it to the Session and Table.
	
	A Read query can be customized with filters and other paramters. Read objects'
	functions return the same Read object, making them chainable:
		query = s.read(tables.USPOI)
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
		filters = dict([(k,v) for k,v in self._filters.iteritems() if v != None])

		params = {
			"filters": self.unparse_dict(filters),
			"limit": self._count
		}

		offset = self._count * (self._page - 1)
		if offset > 0:
			params["offset"] = offset
		
		return self.join_params(params)

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
	def search(self, search_term):
		'''Convenience method to apply a {"$search":...} filter'''
		return self.filter(filter_helpers.search_(search_term))
	def within(self, lat, lon, radius):
		'''Convenience method to apply a $loc/$within/$center filter. Radius is in meters.'''
		return self.filter(filter_helpers.within_(lat, lon, radius))
	def name(self, term):
		'''Convenience method to apply a {"name":...} filter'''
		return self.filter(filter_helpers.eq_("name", term))
class Input(WriteRequest):
	action = "input"
	def __init__(self, session, table):
		Request.__init__(self, session, table)
		self._values = None
		self._comments = None
		self._source = None
		self._subject_key = None
		self._token = None
	def get_query(self):
		# todo: decide whether subject key removal here makes sense
		if 'subject_key' in self._values:
			subject_key = self._values['subject_key']
			del self._values['subject_key']
			if self._subject_key == None:
				self._subject_key = subject_key
		params = {
			"values": self.unparse_dict(self._values),
			"comments": self._comments,
			"source": self._source,
			"subject_key": self._subject_key,
			"token": self._token
			}
		return self.join_params(params)
	def values(self, values):
		'''
		Set the values dictionary to write to the table.

		N.B. Because the subject_key is included in row dicts returned by this library
		     but is also not allowed as a field in a values sumission to Factual's input 
			 action, if 'subject_key' is in the submitted values dict, it will be removed
			 and passed as the subject_key parameter to this edit, unless a different, 
			 non-None subject_key is explicitly specified. 

		     This will make this edit an update rather than an insert. 
		'''
		self._values = values.copy()
		return self
	def source(self, source):
		'''Set a source citation for this edit.'''
		self._source = source
		return self
	def comments(self, comments):
		'''Set a comment for this edit.'''
		self._comments = comments
		return self
	def subject_key(self, subject_key):
		'''
		Set a subject_key of the row to be update.  Setting a subject key causes the 
		input action to be treated as an update rather than an insert.
		'''
		self._subject_key = subject_key
		return self
	def token(self, token):
		'''Set a user's id token as the author of this edit.'''
		self._token = token
		return self
class Rate(WriteRequest):
	action = "rate"
	def __init__(self, session, table):
		Request.__init__(self, session, table)
		self._rating = None
		self._subject_key = None
	def get_query(self):
		return self.join_params({"rating": self._rating, "subject_key": self._subject_key})
	def rating(self, rating):
		'''Set the rating for the specified row.'''
		self._rating = rating
		return self
	def subject_key(self, subject_key):
		'''Set the subject_key of the row to be rated.'''
		self._subject_key = subject_key
		return self
class Duplicates(Request):
	action = "duplicates"
	# todo: create DuplicateResponse 
	#response_type = responses.DuplicateResponse
	def __init__(self, session, table):
		Request.__init__(self, session, table)
		self._values = None
	def get_query(self):
		return self.join_params({"values": self.unparse_dict(self._values)})
	def values(self, values):
		'''Set the values dictionary to be compared against the Factual table.'''
		self._values = values.copy()
		return self
class Schema(Request):
	action = "schema"
	response_type = responses.SchemaResponse
	def get_query(self):
		# schema action takes no parameters
		return ""

