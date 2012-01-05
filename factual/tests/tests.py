'''
Tests for Factual v2 "Server" API wrapper
'''

import factual.v2 as v2
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
	       standard_categories,\
		   standard_categories_with_blank_category,\
		   standard_filters,\
		   standard_filters_with_blank_category
	v2_session = v2.Session(api_key=API_KEY)

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
	query_check_helper(query, 'limit=20&filters={"name":"foobar"}')

def check_or_query(session):
	query = session.read(tables.USPOI).filter(
											common.shared_filter_helpers.or_(
												common.shared_filter_helpers.bw_("category", "Food"), 
												common.shared_filter_helpers.bw_("category", "Arts")
											)
										).search("Foobar")
	query_check_helper(query, \
		'limit=20&filters={"$or":[{"category":{"$bw":"Food"}},{"category":{"$bw":"Arts"}}],"$search":"Foobar"}')

def check_category_filtering(session):
	query = session.read(tables.USPOI)
	query.filter(standard_categories)
	query_check_helper(query, \
		'''limit=20&filters={"$or":[{"category":{"$bw":"Arts,+Entertainment+%26+Nightlife"}},{"category":{"$bw":"Community+%26+Government+%3E+Day+Care+%26+Preschools"}},{"category":{"$bw":"Community+%26+Government+%3E+Dry+Cleaning,+Ironing+%26+Laundry"}},{"category":{"$bw":"Community+%26+Government+%3E+Libraries"}},{"category":{"$bw":"Community+%26+Government+%3E+Religious"}},{"category":{"$bw":"Education"}},{"category":{"$bw":"Food+%26+Beverage"}},{"category":{"$bw":"Legal+%26+Financial+%3E+Banking+%26+Financing"}},{"category":{"$bw":"Personal+Care+%26+Services"}},{"category":{"$bw":"Shopping"}},{"category":{"$bw":"Sports+%26+Recreation"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Airports"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Historical+Sites"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Horse-Drawn+Vehicles"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Lodging"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Monuments"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Parking"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Public+Transportation+%26+Transit"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Railroads+%26+Trains"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Resorts"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Taxi+%26+Car+Services"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Tourist+Attractions"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Wineries+%26+Vineyards"}}]}''')

def check_uuid_lookup(session):
	query = session.read(tables.USPOI)
	query.filter({'factual_id': 'b3b08e30-8e3b-012e-06c9-003048c87378'})
	query_check_helper(query, 'limit=20&filters={"factual_id":"b3b08e30-8e3b-012e-06c9-003048c87378"}')

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
	v2_expected = 'limit=20&filters={"$search":"coffee+and+tea"}'
	yield query_check_helper, v2_query, v2_expected

#	v3_query = v3_session.read(tables.USPOI).search("coffee and tea")
#	v3_expected = 'limit=20&q=coffee+and+tea'
#	yield query_check_helper, v3_query, v3_expected

#### v2 only

def test_v2_geo_query():
	query = v2_session.read(tables.USPOI).search("coffee").within(40.7353,-73.9912,1000)
	query_check_helper(query, \
		'limit=20&filters={"$loc":{"$within":{"$center":[[40.735300,-73.991200],1000]}},"$search":"coffee"}')

def test_v2_category_and_radius_query():
	query = v2_session.read(tables.USPOI)
	query.filter(standard_filters_with_blank_category)
	query.filter(v2.filter_helpers.within_(40.7353, -73.9912, 1500000))
	query_check_helper(query, \
		'''limit=20&filters={"$or":[{"category":{"$bw":"Arts,+Entertainment+%26+Nightlife"}},{"category":{"$bw":"Community+%26+Government+%3E+Day+Care+%26+Preschools"}},{"category":{"$bw":"Community+%26+Government+%3E+Dry+Cleaning,+Ironing+%26+Laundry"}},{"category":{"$bw":"Community+%26+Government+%3E+Libraries"}},{"category":{"$bw":"Community+%26+Government+%3E+Religious"}},{"category":{"$bw":"Education"}},{"category":{"$bw":"Food+%26+Beverage"}},{"category":{"$bw":"Legal+%26+Financial+%3E+Banking+%26+Financing"}},{"category":{"$bw":"Personal+Care+%26+Services"}},{"category":{"$bw":"Shopping"}},{"category":{"$bw":"Sports+%26+Recreation"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Airports"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Historical+Sites"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Horse-Drawn+Vehicles"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Lodging"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Monuments"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Parking"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Public+Transportation+%26+Transit"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Railroads+%26+Trains"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Resorts"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Taxi+%26+Car+Services"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Tourist+Attractions"}},{"category":{"$bw":"Travel+%26+Tourism+%3E+Wineries+%26+Vineyards"}},{"category":{"$blank":true}}],"status":1,"$loc":{"$within":{"$center":[[40.735300,-73.991200],1500000]}}}''')


#### v3 only

#def test_v3_geo_query_compat():
#	# old style "within" compat
#	query = v3_session.read("places").search("coffee").within(40.7353,-73.9912,1000)
#def test_v3_geo_query_new_style():
#	# new style circle
#	query = v3_session.read("places").search("coffee").filter({"$circle":{"$center":[40.7353,-73.9912], "$meters":1000}})