import logging

import oauth2

import requests
import factual.common.session

class Session(factual.common.session.BaseSession):
	_url_pat = "%(api_base)s/t/%(table_id)s/%(action)s?%(query)s"
	def __init__(
				self, 
				consumer_key=None, 
				consumer_secret=None, 
				api_key=None, # deprecated
				api_base="http://api.v3.factual.com"
				):
		'''
		Construct a Session object to hold OAuth credentials. Provide an OAuth consumer 
		key and consumer secret to use with the Factual API.

		n.b. Providing only an api_key or only a consumer_key will fall back to 
		     authenticating requests via the KEY query string parameter, skipping 
			 OAuth entirely. This behavior is deprecated in the v3 API. 
		'''
		self.consumer_key = consumer_key if consumer_key else api_key
		self.consumer_secret = consumer_secret
		self.api_base = api_base

		if api_key:
			logging.warn("The api_key parameter is deprecated in the v3 API. Use OAuth.")

		if self.consumer_secret:
			self.consumer = oauth2.Consumer(consumer_key, consumer_secret)
			self.oauth_signature_method = oauth2.SignatureMethod_HMAC_SHA1()
		else:
			self.consumer = None
			logging.warn("Non-OAuth requests are deprecated in the v3 API. Pass both a consumer key and secret to use OAuth.")

	def get_url(self, request):
		query = request.get_query()
		if not self.consumer:
			# fall back to api_key behavior
			query = "%s&KEY=%s" % (query, self.consumer_key,)
		return self._url_pat % {
				'api_base': self.api_base,
				'table_id': request.table,
				'action':   request.action,
				'query':    query
			}
	def get_headers(self, request, defaults={}):
		headers = {}
		if self.consumer:
			# only do OAuth if we have a consumer_secret to use, else fall back to api_key in URL

			# todo: check that Factual API is always GET/blank body/not form encoded
			oauth_request = oauth2.Request.from_consumer_and_token(
								consumer=self.consumer,
								token=None,

								http_method="GET",
								body="",
								is_form_encoded=False,

								http_url=self.get_url(request),
								parameters=None
								)

			# pass None as the Token since Factual's API is 2-legged OAuth only
			oauth_request.sign_request(self.oauth_signature_method, self.consumer, None)
			headers.update(oauth_request.to_header())
		headers.update(defaults)
		return headers
	def read(self, table):
		'''Build a Read request on the provided Table type using this Session. See the requests module for details.'''
		return requests.Read(self, table)

