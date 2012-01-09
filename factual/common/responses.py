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
			error = "\"%s\" error: %s" % (body.get("error_type"), body.get("message"))
			raise exceptions.FactualError(error)
	def __repr__(self):
		if len(self.response) > 3:
			response_repr = "%d records in response" % len(self.response)
		else:
			response_repr = self.response.__repr__()
		return "FactualResponse(%s, v%s, %s)" % (self.status, self.version, response_repr)
class ReadResponse(Response):
	pass
class SchemaResponse(Response):
	pass

