'''
Tests for Factual v2 "Server" API wrapper
'''

import nose
from nose.tools import eq_

import factual.v2 as v2
import factual.v3 as v3
import factual.common as common
from factual.v2 import tables

categories = [
	'Sports & Recreation > Gyms & Fitness Centers',
	'Food & Beverage > Bakeries',
	'Arts, Entertainment & Nightlife > Social Clubs',
	'Travel & Tourism > Parking',
	'Food & Beverage > Kosher',
	'Arts, Entertainment & Nightlife > Comedy Clubs',
	'Arts, Entertainment & Nightlife > Karaoke',
	'Arts, Entertainment & Nightlife > Bingo Halls',
	'Food & Beverage > Ethnic Food',
	'Sports & Recreation',
	'Personal Care & Services',
	'Arts, Entertainment & Nightlife > Billiard Parlors & Pool Halls',
	'Travel & Tourism > Resorts',
	'Food & Beverage > Cafes, Coffee Houses & Tea Houses',
	'Arts, Entertainment & Nightlife > Movie Theatres',
	'Food & Beverage > Beer, Wine & Spirits',
	"Food & Beverage > Farmers' Markets",
	'Community & Government > Libraries',
	'Arts, Entertainment & Nightlife > Concert Halls & Theaters',
	'Food & Beverage > Bagels & Donuts',
	'Shopping',
	'Arts, Entertainment & Nightlife > Museums',
	'Arts, Entertainment & Nightlife > Adult Entertainment',
	'Arts, Entertainment & Nightlife > Bars',
	'Arts, Entertainment & Nightlife > Orchestras, Symphonies & Bands',
	'Arts, Entertainment & Nightlife > Bowling Alleys',
	'Food & Beverage > Chocolate',
	'Travel & Tourism > Tourist Attractions',
	'Arts, Entertainment & Nightlife > Night Clubs',
	'Arts, Entertainment & Nightlife > Ticket Sales',
	'Travel & Tourism > Railroads & Trains',
	'Travel & Tourism > Horse-Drawn Vehicles',
	'Sports & Recreation > Zoos, Aquariums & Wildlife Sanctuaries',
	'Community & Government > Day Care & Preschools',
	'Community & Government > Dry Cleaning, Ironing & Laundry',
	'Travel & Tourism > Public Transportation & Transit',
	'Travel & Tourism > Monuments',
	'Food & Beverage > Breweries',
	'Arts, Entertainment & Nightlife > Casinos & Gaming',
	'Food & Beverage > Cheese',
	'Food & Beverage > Restaurants',
	'Food & Beverage > Dessert',
	'Travel & Tourism > Lodging',
	'Legal & Financial > Banking & Financing',
	'Arts, Entertainment & Nightlife > Psychics & Astrologers',
	'Sports & Recreation > Yoga & Pilates',
	'Food & Beverage > Juice Bars & Smoothies',
	'Food & Beverage > Health & Diet Food',
	'Travel & Tourism > Taxi & Car Services',
	'Arts, Entertainment & Nightlife > Hookah Lounges',
	'Travel & Tourism > Wineries & Vineyards',
	'Arts, Entertainment & Nightlife > Jazz & Blues Cafes',
	'Arts, Entertainment & Nightlife',
	'Travel & Tourism > Airports',
	'Travel & Tourism > Historical Sites',
	'Arts, Entertainment & Nightlife > Art Dealers & Galleries',
	'Sports & Recreation > Personal Trainers',
	'Food & Beverage',
	'Community & Government > Religious',
	'Arts, Entertainment & Nightlife > Internet Cafes',
	'Education',
	'Food & Beverage > Ice Cream Parlors',
	'Sports & Recreation > Sports Clubs',
	'Arts, Entertainment & Nightlife > Arcades & Amusement Parks'
	]


API_KEY='deadbeef'

def setup():
	global v2_session,\
	       v3_session,\
	       standard_categories,\
		   standard_categories_with_blank_category,\
		   standard_filters,\
		   standard_filters_with_blank_category
	v2_session = v2.Session(api_key=API_KEY)
	v3_session = v3.Session(api_key=API_KEY)

	standard_categories = common.category_helpers.make_category_filter(categories,blank=False)
	standard_categories_with_blank_category = common.category_helpers.make_category_filter(categories,blank=True)

	standard_filters = standard_categories.copy()
	standard_filters['status'] = 1

	standard_filters_with_blank_category = standard_categories_with_blank_category.copy()
	standard_filters_with_blank_category['status'] = 1

def query_check_helper(query, expected):
	print "query:\n%s\nexpected:\n%s" % (query.get_query(), expected)
	assert query.get_query() == expected 

def check_name_query(session):
	query = session.read(tables.USPOI).filter({"name":"foobar"})
	query_check_helper(query, 'limit=20&filters={%22name%22:%22foobar%22}')

def check_or_query(session):
	query = session.read(tables.USPOI).filter(
											common.shared_filter_helpers.or_(
												common.shared_filter_helpers.bw_("category", "Food"), 
												common.shared_filter_helpers.bw_("category", "Arts")
											)
										).search("Foobar")
	query_check_helper(query, \
		'limit=20&filters={%22$or%22:[{%22category%22:{%22$bw%22:%22Food%22}},{%22category%22:{%22$bw%22:%22Arts%22}}],%22$search%22:%22Foobar%22}')

def check_category_filtering(session):
	query = session.read(tables.USPOI)
	query.filter(standard_categories)
	query_check_helper(query, \
		'''limit=20&filters={%22$or%22:[{%22category%22:{%22$bw%22:%22Arts,+Entertainment+%26+Nightlife%22}},{%22category%22:{%22$bw%22:%22Community+%26+Government+%3E+Day+Care+%26+Preschools%22}},{%22category%22:{%22$bw%22:%22Community+%26+Government+%3E+Dry+Cleaning,+Ironing+%26+Laundry%22}},{%22category%22:{%22$bw%22:%22Community+%26+Government+%3E+Libraries%22}},{%22category%22:{%22$bw%22:%22Community+%26+Government+%3E+Religious%22}},{%22category%22:{%22$bw%22:%22Education%22}},{%22category%22:{%22$bw%22:%22Food+%26+Beverage%22}},{%22category%22:{%22$bw%22:%22Legal+%26+Financial+%3E+Banking+%26+Financing%22}},{%22category%22:{%22$bw%22:%22Personal+Care+%26+Services%22}},{%22category%22:{%22$bw%22:%22Shopping%22}},{%22category%22:{%22$bw%22:%22Sports+%26+Recreation%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Airports%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Historical+Sites%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Horse-Drawn+Vehicles%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Lodging%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Monuments%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Parking%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Public+Transportation+%26+Transit%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Railroads+%26+Trains%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Resorts%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Taxi+%26+Car+Services%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Tourist+Attractions%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Wineries+%26+Vineyards%22}}]}''')

def check_uuid_lookup(session):
	query = session.read(tables.USPOI)
	query.filter({'factual_id': 'b3b08e30-8e3b-012e-06c9-003048c87378'})
	query_check_helper(query, 'limit=20&filters={%22factual_id%22:%22b3b08e30-8e3b-012e-06c9-003048c87378%22}')

#### Shared test generators
#
# Run these tests/checks against both the v2 and v3 apis.
#

# Should have identical results.
def test_name_query():
	for session in [ v2_session ]:
		yield check_name_query, session

def test_or_query():
	for session in [ v2_session ]:
		yield check_or_query, session

def test_category_filtering():
	for session in [ v2_session ]:
		yield check_category_filtering, session

def test_uuid_lookup():
	for session in [ v2_session ]:
		yield check_uuid_lookup, session

# These will differ as noted:
def test_search_query():
	v2_query = v2_session.read(tables.USPOI).search("coffee and tea")
	v2_expected = 'limit=20&filters={%22$search%22:%22coffee+and+tea%22}'
	yield query_check_helper, v2_query, v2_expected

#	v3_query = v3_session.read(tables.USPOI).search("coffee and tea")
#	v3_expected = 'limit=20&q=coffee+and+tea'
#	yield query_check_helper, v3_query, v3_expected

def test_url_from_table_type():
	v2_query = v2_session.read(tables.USPOI)
	eq_(v2_session.get_url(v2_query), 'http://api.factual.com/v2/tables/s4OOB4/read?api_key=deadbeef&limit=20')
def test_url_from_table_instance():
	v2_query = v2_session.read(tables.USPOI())
	eq_(v2_session.get_url(v2_query), 'http://api.factual.com/v2/tables/s4OOB4/read?api_key=deadbeef&limit=20')
def test_url_from_table_parent_instance():
	v2_query = v2_session.read(common.util.Table("s4OOB4"))
	eq_(v2_session.get_url(v2_query), 'http://api.factual.com/v2/tables/s4OOB4/read?api_key=deadbeef&limit=20')
def test_url_from_table_string():
	v2_query = v2_session.read("s4OOB4")
	eq_(v2_session.get_url(v2_query), 'http://api.factual.com/v2/tables/s4OOB4/read?api_key=deadbeef&limit=20')

def test_v3_url_from_table_parent_instance():
	v3_query = v3_session.read(common.util.Table("places"))
	eq_(v3_session.get_url(v3_query), 'http://api.v3.factual.com/t/places/read?limit=20&KEY=deadbeef')
def test_v3_url_from_table_string():
	v3_query = v3_session.read("places")
	eq_(v3_session.get_url(v3_query), 'http://api.v3.factual.com/t/places/read?limit=20&KEY=deadbeef')

#### v2 only

def test_v2_geo_query():
	query = v2_session.read(tables.USPOI).search("coffee").within(40.7353,-73.9912,1000)
	query_check_helper(query, \
		'limit=20&filters={%22$loc%22:{%22$within%22:{%22$center%22:[[40.735300,-73.991200],1000]}},%22$search%22:%22coffee%22}')

	print v2_session.get_url(query)

def test_v2_category_and_radius_query():
	query = v2_session.read(tables.USPOI)
	query.filter(standard_filters_with_blank_category)
	query.filter(v2.filter_helpers.within_(40.7353, -73.9912, 1500000))
	query_check_helper(query, \
		'''limit=20&filters={%22$or%22:[{%22category%22:{%22$bw%22:%22Arts,+Entertainment+%26+Nightlife%22}},{%22category%22:{%22$bw%22:%22Community+%26+Government+%3E+Day+Care+%26+Preschools%22}},{%22category%22:{%22$bw%22:%22Community+%26+Government+%3E+Dry+Cleaning,+Ironing+%26+Laundry%22}},{%22category%22:{%22$bw%22:%22Community+%26+Government+%3E+Libraries%22}},{%22category%22:{%22$bw%22:%22Community+%26+Government+%3E+Religious%22}},{%22category%22:{%22$bw%22:%22Education%22}},{%22category%22:{%22$bw%22:%22Food+%26+Beverage%22}},{%22category%22:{%22$bw%22:%22Legal+%26+Financial+%3E+Banking+%26+Financing%22}},{%22category%22:{%22$bw%22:%22Personal+Care+%26+Services%22}},{%22category%22:{%22$bw%22:%22Shopping%22}},{%22category%22:{%22$bw%22:%22Sports+%26+Recreation%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Airports%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Historical+Sites%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Horse-Drawn+Vehicles%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Lodging%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Monuments%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Parking%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Public+Transportation+%26+Transit%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Railroads+%26+Trains%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Resorts%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Taxi+%26+Car+Services%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Tourist+Attractions%22}},{%22category%22:{%22$bw%22:%22Travel+%26+Tourism+%3E+Wineries+%26+Vineyards%22}},{%22category%22:{%22$blank%22:true}}],%22status%22:1,%22$loc%22:{%22$within%22:{%22$center%22:[[40.735300,-73.991200],1500000]}}}''')


#### v3 only

def test_v3_geo_query_compat():
	# old style "within" compat
	query = v3_session.read("places").search("coffee").within(40.7353,-73.9912,1000)
	query_check_helper(query, 'q=coffee&geo={%22$circle%22:{%22$center%22:[40.735300,-73.991200],%22$meters%22:1000}}&limit=20')

	print v3_session.get_url(query)

#def test_v3_geo_query_new_style():
#	# new style circle
#	query = v3_session.read("places").search("coffee").filter({"$circle":{"$center":[40.7353,-73.9912], "$meters":1000}})
