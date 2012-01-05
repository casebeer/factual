'''
v2 Tables
'''

from factual.common.util import Table

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
