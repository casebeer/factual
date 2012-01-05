import logging

from factual.common import exceptions
from factual.common.responses import Response

class V2ReadResponse(Response):
	def __init__(self, body, meta=None):
		Response.__init__(self, body, meta)
		self.data = self.response.get("data", None)
		self.fields = self.response.get("fields", None)
		self._records = None
	def _process_row(self, row):
		# todo: wrap record in custom dict subclass? keep field references?
		record = {}
		for i in range(len(self.fields)):
			record[self.fields[i]] = row[i]
		return record
	def _get_records(self):
		return [self._process_row(row) for row in self.data]
	def records(self):
		'''Return a list of dicts corresponding to the data returned by Factual.'''
		if self._records == None:
			self._records = self._get_records()
		return self._records
class V2SchemaResponse(Response):
	def __init__(self, body, meta=None):
		Response.__init__(self, body, meta)
		self.schema = self.body.get("schema", {})

