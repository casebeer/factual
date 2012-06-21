import logging

import requests
import tables
import factual.common.session

class Session(factual.common.session.BaseSession):
	def read(self, table):
		'''Build a Read request on the provided Table type using this Session. See the requests module for details.'''
		return requests.Read(self, table)
	def input(self, table):
		'''Build an Input request on the provided Table type using this Session. See the requests module for details.'''
		return requests.Input(self, table)
	def rate(self, table):
		'''Build a Rate request on the provided Table type using this Session. See the requests module for details.'''
		return requests.Rate(self, table)
	def duplicates(self, table):
		'''Build a Duplicates request on the provided Table type using this Session. See the requests module for details.'''
		return requests.Duplicates(self, table)
	def schema(self, table):
		'''Build a Schema request on the provided Table type using this Session. See the requests module for details.'''
		return requests.Schema(self, table)

