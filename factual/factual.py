import httplib2
import urllib
import simplejson
import logging
logging.basicConfig(level=logging.DEBUG)
import UserDict
import os
import pkg_resources
import csv
import unidecode
import datetime
import time

import config

US_BUS="s4OOB4"
API_KEY=config.conf.get('factual', 'api_key')

### Factual filter functions
# todo: move to module

def prep_term(term):
	# ensure dates are converted to epoch if needed
	if type(term)==datetime.datetime:
		term = time.mktime(term)
	return term

# generic filters
def or_(*args):
	return {"$or": args}
def and_(*args):
	return {"$and": args}
def field_filter(op, field, term):
	return {field: {op: prep_term(term)}}
# text and numeric ops
def eq_(field, term):
	return {field: prep_term(term)}
def neq_(field, term):
	return field_filter("$neq", field, term)
def in_(field, terms):
	if type(terms) != list:
		terms = [terms]
	return field_filter("$in", field, terms)
def blank_(field):
	return field_filter("$blank", field, True)
def not_blank_(field):
	return field_filter("$blank", field, False)
# text ops
def bw_(field, term):
	return field_filter("$bw", field, term)
def search_(term):
	return {"$search": term}
# geo ops
def within_(lat, lon, radius=1500):
	return {"$loc": {"$within": {"$center":[[lat, lon], radius]}}}
# numeric ops
def gt_(field, term):
	return field_filter("$gt", field, term)
def gte_(field, term):
	return field_filter("$gte", field, term)
def lt_(field, term):
	return field_filter("$lt", field, term)
def lte_(field, term):
	return field_filter("$lte", field, term)

class FactualRequest(object):
	def __init__(self, filters={}, limit=50, api_key=API_KEY, table_id=US_BUS):
		self._filters = filters
		self._limit = limit
		self.api_key = api_key
		self.table_id = table_id

	def get_url(self):
		filters = dict([(k,v) for k,v in self._filters.iteritems() if v != None])
		params = {
			"filters": urllib.quote(unidecode.unidecode(\
							simplejson.dumps(filters,ensure_ascii=False, \
									separators=(',',':'))), \
								'/{}"$:,[]'),
			"limit": self._limit
		}
		param_str = "&".join([("%s=%s" % (k,v)) for k,v in params.iteritems()])
		url = self._url_pat % ({
						'TABLE_ID':self.table_id, 
						'API_KEY':self.api_key,
						'PARAMS': param_str
						})
		return url
	
	def get_filters(self):
		return self._filters
	def set_filters(self, filters):
		self._filters = filters
	filters = property(get_filters, set_filters)

	def limit(self, limit):
		self._limit = limit
		return self #chainable
	
	def filter(self, filter):
		self._filters.update(filter)
		return self # chainable
	def search(self, search_term):
		'''Convenience method to apply a {"$search":...} filter'''
		return self.filter(search_(search_term))
	def within(self, lat, lon, radius):
		return self.filter(within_(lat, lon, radius))
	def name(self, term):
		return self.filter(eq_("name", "term"))
		
	def GET(self):
		'''
		Note: this function can raise JsonDecode exceptions if Factual doesn't provide 
		valid JSON – as when they are doing maintenance. 
		'''
		url = self.get_url()
		logging.debug(url)
		h = httplib2.Http()
		resp, body = h.request(url)
		return simplejson.loads(body)
	_url_pat = "http://api.factual.com/v2/tables/%(TABLE_ID)s/read?api_key=%(API_KEY)s&%(PARAMS)s"

class FactualResponse(object):
	def __init__(self, body, field_map=None):
		self._status = body.get("status", None)
		self._version = body.get("version", None)
		self._response = body.get("response", None)
		self._data = self._response.get("data", None)
		self._fields = self._response.get("fields", None)
		if field_map == None:
			self._field_map = dict([(f,f) for f in self._fields])
			self._mapped_fields = self._fields
		else:
			# rebuild map to ensure all fields covered
			self._field_map = {}
			self._mapped_fields = []
			for field in self._fields:
				self._field_map[field] = field_map.get(field, None)
				self._mapped_fields.append(field_map.get(field, None))
	def _process_record(self, record):
		r = {}
		for i in range(len(self._mapped_fields)):
			field = self._mapped_fields[i]
			if field == None:
				continue # skip field if suppressed by map
			r[field] = record[i]
		return r
	def records(self):
		return [self._process_record(record) for record in self._data]

class FactualSearch(FactualRequest):
	def __init__(self,
				search=None,
				city=None,
				name=None,
				geo=None,
				radius=1500,
				filters={},
				api_key=API_KEY,
				table_id=US_BUS):
		ret = FactualRequest.__init__(self)
		self.search = search
		self.city = city
		self.name = name
		self.geo = geo
		self.radius = radius
		return ret
	def get_filters(self):
		filters = { }
		if self.search:
			filters['$search'] = self.search
		if self.name:
			filters['name'] = self.name
		if self.city:
			filters['city'] = self.city
		if self.geo:
			filters['$loc'] = {
								'$within': { 
									'$center': [self.geo[0], self.geo[1], self.radius]
								}
							}
		return filters

def get_factual_businesses(lat, lon, dist=1500):
	filters = {
		'$and':[
			{'$loc':{
				'$within': {
					'$center': [lat, lon, dist]
				}
			}},
			{'status':'1'},
			category_map.filters
		]
	}
	req = FactualRequest(api_key=API_KEY, table_id=US_BUS, filters=filters)
	return req.GET()

class FactualCategoryMap(dict):
	def __init__(self, data):
		self.filter_cats = []
		for row in data:
			fields = [x.strip() for x in row]

			factual_label = fields[0]
			pm_label = fields[1]

			cats = [x.strip() for x in factual_label.split('>',1)]
			factual_cat = cats[0]
			factual_subcat = None
			if len(cats) > 1:
				factual_subcat = cats[1]

			if factual_subcat == 'CATCHALL':
				factual_label = factual_cat
			self.filter_cats.append(factual_label)
			self[factual_label] = pm_label

		self.filters = {'$or':[{'category': {'$bw':cat}} for cat in \
						shortest_prefixes(self.filter_cats)]}

def shortest_prefixes(list):
	list.sort()

	to_remove = []
	prev = None
	for item in list:
		if prev != None and item.find(prev) == 0:
			to_remove.append(item)
		else:
			prev = item
	for item in to_remove:
		list.remove(item)
	return list


def map_category(fc):
	if fc in category_map:
		return category_map[fc]
	if fc == None:
		return None
	cats = fc.split('>',1)
	cat = cats[0]
	cat = cat.strip()
	if cat in category_map:
		return category_map[cat]
	return None

class FactualPlace(UserDict.DictMixin):
	direct_map = {
		'factual_uuid': 'uuid',
		 'name': 'name',
		 'address1': 'address',
		 'city': 'locality',
		 'region': 'region',
		 'country': 'country',
		 'postal_code': 'postcode',
		 'phone': 'tel',
		 'fax': 'fax',
		 'website': 'website',
		 'lat': 'latitude',
		 'lon': 'longitude'
	}
	def __init__(self, data):
		# factual_uuid, name, address, city, region, postal_code, phone, fax, category, website, lat, lon
		self.factual = {}
		# todo: map fields from the fields dict provided along with the factual API results
		self.factual['dbid'], self.factual['uuid'], self.factual['name'], self.factual['address'], \
			self.factual['address_extended'], self.factual['po_box'], self.factual['locality'], \
			self.factual['region'], self.factual['country'], self.factual['postcode'], self.factual['tel'], self.factual['fax'], \
			self.factual['category'], self.factual['website'], self.factual['email'], \
			self.factual['latitude'], self.factual['longitude'], self.factual['status'] = data
	def _get_category(self):
		fc = self.factual.get('category', None)
		return map_category(fc)
	def __getitem__(self, key):
		if key in self.direct_map:
			return self.factual[self.direct_map[key]]
		if key == 'category':
			return self._get_category()
	def keys(self):
		keys = self.direct_map.keys()
		keys.append('category')
		return keys

def get_places(lat, lon, dist=1500):
	places = []
	res = get_factual_businesses(lat, lon, dist)

	for place in res['response']['data']:
		places.append(FactualPlace(place))
	return places
	
def good_places(places):
	return [place for place in places if place['category'] != None]

def bad_cats(places):
	return [(place['name'], place.factual['category']) for place in places if place['category'] == None]

# pull in category mapping config
reader = csv.reader(pkg_resources.resource_stream(__name__, 'data/factual_category_map.csv'))
category_map = FactualCategoryMap(reader)

if __name__ == '__main__':
	import optparse
	from pprint import pprint 

	lat, lon = 40.73946, -73.98487

	parser = optparse.OptionParser()
	parser.add_option('-i', '--interactive', 
				action='store_true', 
				dest='interactive')
	(options, args) = parser.parse_args()

	if options.interactive:
		import code
		code.interact(local=locals())
	else:
		places = get_places(lat, lon)

		pprint(good_places(places))

		print """
			Places: %d
			Good places: %d
		""" % (len(places), len(good_places(places)))
		pprint(bad_cats(places))


