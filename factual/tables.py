'''
Table classes hold information about Factual tables. 

At the moment, their only purpose is to hold the table's ID for the Session
to use in building API URLs. 

To use a new Factual table, subclass Table and set _table_id as a class variable
holding the new table's ID. 

'''

class Table(object):
	_table_id = None
	def __init__(self, id=None):
		self._id = id
		# todo: query and cache schema for table?
	def _get_id(self):
		if self._id:
			return self._id
		else:
			return self._table_id
	id = property(_get_id)

class USPOI(Table):
	'''
	US POI and Business Listings table
	http://www.factual.com/t/s4OOB4/US_POI_and_Business_Listings
	'''
	_table_id = "s4OOB4"

class USLocalPlaypen(Table):
	'''
	Playpen for U.S. local data table for experimenting with API calls
	http://www.factual.com/t/Nj0JN3/POI_and_Local_sandbox_Los_Angeles_CA
	'''
	_table_id = "Nj0JN3"

class AULocalPlaypen(Table):
	'''
	Playpen for Australian local data
	http://www.factual.com/t/eN7l2X/Sydney_POI_and_Business_Listings_API_PLAYGROUND
	'''
	_table_id = "eN7l2X"
