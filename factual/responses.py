import logging
import exceptions

class Response(object):
	def __init__(self, body, meta=None):
		self.meta = meta
		self.body = body

		# todo: handle non-"ok" status
		self.status = body.get("status", None)
		self.version = body.get("version", None)
		self.response = body.get("response", {})

		if self.status == "error":
			raise exceptions.FactualError(body.get("error"))
	def __repr__(self):
		if len(self.response) > 3:
			response_repr = "%d records in response" % len(self.response)
		else:
			response_repr = self.response.__repr__()
		return "FactualResponse(%s, v%s, %s)" % (self.status, self.version, response_repr)
class ReadResponse(Response):
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
class SchemaResponse(Response):
	def __init__(self, body, meta=None):
		Response.__init__(self, body, meta)
		self.schema = self.body.get("schema", {})
