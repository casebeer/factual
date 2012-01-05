'''
Helper functions to handle Factual point of interest category queries and mappings.

These functions assume that the user (a) wants to limit results to the smallest
set of catgories matching a predefined list and (b) wants to map Factual's category
labels into his own category labelling system. 
'''

import shared_filter_helpers as ops

def make_category_filter(categories, blank=True):
	'''
	Generates a dict representing a Factual filter matching any of the categories
	passed. 

	The resulting filter uses $bw "begins with" operators to return all matching
	subcategories. Because of this, passing a top level category removes the need
	to pass any of its subcategories. 

	Conversely, specifying subcategories will not restrict results as expected
	if a prefix of those subcategories is also provided. For example:
		make_category_filter(["Food & Beverage", "Food & Beverage > Cheese"])
	is the same as 
		make_category_filter(["Food & Beverage"])
	
	To minimize the size of the filters sent to Factual, make_category_filters 
	identifies redundant subcategories and removes them. 

	Note that because of this prefix matching, queries may return rows from unwanted
	subcategories. It may be necessary for you to filter out these records after 
	the Factual request. 

	Specify blank=True to include items without a category set.
	'''
	categories = [category.strip() for category in categories]

	# find shortest prefixes
	categories.sort()
	redundant_categories = set()
	prefix_candidate = None
	for category in categories:
		if prefix_candidate != None \
			and category.find(prefix_candidate) == 0:
			# prefix_candidate is a prefix of the current category, 
			# so we can skip the current category
			redundant_categories.add(category)
		else:
			prefix_candidate = category
	categories = [category for category in categories if category not in redundant_categories]

	filters = [ops.bw_("category", category) for category in categories]
	if blank:
		filters.append(ops.blank_("category"))
	return ops.or_(*filters)

