import logging
import httplib2
try:
	import simplejson as json
except ImportError:
	import json

import requests
import factual.common.session

class Session(factual.common.session.BaseSession):
	_url_pat = "%(api_base)s/t/%(table_id)s/%(action)s?KEY=%(api_key)s&%(query)s"
	def __init__(self, api_key=None, api_base="http://api.v3.factual.com"):
		'''Provide an api_key to use with the Factual API.'''
		self.api_key = api_key
		self.api_base = api_base
#	def get_url(self, request):
#		return self._url_pat % {
#				'api_base': self.api_base,
#				'table_id': request.table,
#				'action':   request.action,
#				'api_key':  self.api_key,
#				'query':    request.get_query()
#			}
#	def get_headers(self, request):
#		return {}
	def read(self, table):
		'''Build a Read request on the provided Table type using this Session. See the requests module for details.'''
		return requests.Read(self, table)

