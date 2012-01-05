import datetime
import time

class GeoScalar(float):
	'''Class to wrap floats used for geo coords in order to get pretty formatting from simplejson.'''
	def __repr__(self):
		return "%0.6f" % (self)

### Factual filter functions
def _prep_factual_term(term):
	# ensure dates are converted to epoch
	if type(term)==datetime.datetime:
		term = time.mktime(term)
	return term

# generic filters
def or_(*args):
	return {"$or": args}
def and_(*args):
	return {"$and": args}
def field_filter(op, field, term):
	return {field: {op: _prep_factual_term(term)}}
# text and numeric ops
def eq_(field, term):
	return {field: _prep_factual_term(term)}
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

# numeric ops
def gt_(field, term):
	return field_filter("$gt", field, term)
def gte_(field, term):
	return field_filter("$gte", field, term)
def lt_(field, term):
	return field_filter("$lt", field, term)
def lte_(field, term):
	return field_filter("$lte", field, term)
