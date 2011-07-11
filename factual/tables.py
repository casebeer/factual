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
	_table_id = "s4OOB4"

class USLocalPlaypen(Table):
	_table_id = "Nj0JN3"

class AULocalPlaypen(Table):
	_table_id = "eN7l2X"


