def abstract():
	# http://norvig.com/python-iaq.html
	import inspect
	caller = inspect.getouterframes(inspect.currentframe())[1][3]
	raise NotImplementedError(caller + ' must be implemented in subclass')


class Table(object):
	'''
	Table classes hold information about Factual tables. 

	At the moment, their only purpose is to hold the table's ID for the Session
	to use in building API URLs. 

	To use a new Factual table, subclass Table and set _table_id as a class variable
	holding the new table's ID. 

	'''
	_table_id = None
	def __init__(self, id=None):
		self._id = id
		# todo: query and cache schema for table?
	def __repr__(self):
		return self.id
	def _get_id(self):
		if self._id:
			return self._id
		else:
			return self._table_id
	id = property(_get_id)
