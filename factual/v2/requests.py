
import factual.common.requests
from factual.common.requests import Read
import responses
import filter_helpers

class Read(factual.common.requests.Read):
	'''Override response_type with correct ReadResponse type'''
	response_type = responses.V2ReadResponse
	def search(self, search_term):
		'''Convenience method to apply a {"$search":...} filter'''
		return self.filter(filter_helpers.search_(search_term))
	def within(self, lat, lon, radius):
		'''Convenience method to apply a $loc/$within/$center filter. Radius is in meters.'''
		return self.filter(filter_helpers.within_(lat, lon, radius))

class Input(factual.common.requests.WriteRequest):
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
class Rate(factual.common.requests.WriteRequest):
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
class Duplicates(factual.common.requests.Request):
	action = "duplicates"
	# todo: create DuplicateResponse 
	#response_type = responses.V2DuplicateResponse
	def __init__(self, session, table):
		Request.__init__(self, session, table)
		self._values = None
	def get_query(self):
		return self.join_params({"values": self.unparse_dict(self._values)})
	def values(self, values):
		'''Set the values dictionary to be compared against the Factual table.'''
		self._values = values.copy()
		return self

