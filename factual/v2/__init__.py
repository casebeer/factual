'''
Factual Server API  Wrapper
===========================

This package wraps the Factual "Server" API. Its query style is SQLAlchemy-inspired and designed
to make it easy to build "read" requests by chaining filter calls together. 

API actions other than "read" are supported via the same syntax for consistency. 

Basic Usage:

    from factual import *
	from factual.v2.tables import USPOI,USLocalPlaypen
    s = Session(api_key="deadbeef")
    my_place = s.read(USPOI).search("coffee").run().records()[0]
    
    # you can also build requests one piece at a time:
    query = s.read(USPOI)
    query.filter({"name": "Foobar"})
	if test_address != None:
		query.filter({"address": test_address})
    response = query.run()
    records = response.records()
    
    # limiting categories and using the filter helper functions:
    from factual.v2.filter_helpers import *
    q = s.read(USPOI).filter(or_(bw_("category", "Food"), bw_("category", "Arts")))
    q.search("Foobar")
    records = q.run().records()
    
    # geo queries:
    coffee_places = s.read(USPOI).search("coffee").within(40.7353,-73.9912,1000).run().records()
    
    # modify a record in the Playpen:
    p = s.read(USLocalPlaypen).search("coffee").count(1).run().records()[0]
    p['address'] += "/Foobar"
    s.input(USLocalPlaypen).values(p).comment("Silly update test").run()

See also the session.Session and requests.Read documentation.
'''

import logging
logging.basicConfig(level=logging.DEBUG)

from session import Session
import filter_helpers
import factual.common.category_helpers as category_helpers
import tables

