
import factual
from factual.filter_helpers import *

API_KEY='deadbeef'

def setup():
	global s
	s = factual.Session(api_key=API_KEY)

def query_check_helper(query, expected):
	print "query:\n%s\nexpected:\n%s" % (query.get_query(), expected)
	assert query.get_query() == expected 

def test_search_query():
	query = s.read(factual.tables.USPOI).search("coffee")
	query_check_helper(query, 'limit=20&filters={"$search":"coffee"}')

def test_name_query():
	query = s.read(factual.tables.USPOI).filter({"name":"foobar"})
	query_check_helper(query, 'limit=20&filters={"name":"foobar"}')

def test_or_query():
	query = s.read(factual.tables.USPOI).filter(
											or_(
												bw_("category", "Food"), 
												bw_("category", "Arts")
											)
										).search("Foobar")
	query_check_helper(query, \
		'limit=20&filters={"$or":[{"category":{"$bw":"Food"}},{"category":{"$bw":"Arts"}}],"$search":"Foobar"}')

def test_geo_query():
	query = s.read(factual.tables.USPOI).search("coffee").within(40.7353,-73.9912,1000)
	query_check_helper(query, \
		'limit=20&filters={"$loc":{"$within":{"$center":[[40.735300000000002,-73.991200000000006],1000]}},"$search":"coffee"}')

