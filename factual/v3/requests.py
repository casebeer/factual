
import factual.common.requests
from factual.common.requests import Read
import responses
import filter_helpers

class Read(factual.common.requests.Read):
	'''Override response_type with correct ReadResponse type'''
	response_type = responses.V3ReadResponse
	def __init__(self, session, table):
		factual.common.requests.Read.__init__(self, session, table)
		self._geo = {}
		self._search = None
	def get_params(self):
		params = factual.common.requests.Read.get_params(self)
		params["geo"] = self.unparse_dict(self._geo) if self._geo != {} else None
		params["q"] = self._search
		return params
	def search(self, search_term):
		'''
		Apply a "q=..." search filter. Separate terms with commas for OR queries. 
		Subsequent search() calls replace any previous search terms on this query.
		'''
		self._search = search_term
		return self
	def within(self, lat, lon, radius):
		'''
		Apply a geo=$circle/$center filter. Radius is in meters. Subsequent within() 
		calls replace earlier geo filters on this query.
		'''
		self._geo = { "$circle": { 
						"$center": [
							factual.common.shared_filter_helpers.GeoScalar(lat), 
							factual.common.shared_filter_helpers.GeoScalar(lon), 
							], 
						"$meters": radius 
						}
					}
		return self

