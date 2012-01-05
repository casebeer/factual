import logging

from factual.common import exceptions
from factual.common.responses import Response

class V3ReadResponse(Response):
	def __init__(self, body, meta=None):
		Response.__init__(self, body, meta)
		self._data = self.response.get("data", None)
	def records(self):
		'''Return a list of dicts corresponding to the data returned by Factual.'''
		return self._data
class V3SchemaResponse(Response):
	def __init__(self, body, meta=None):
		Response.__init__(self, body, meta)
		self.view = self.response.get("view", {})

