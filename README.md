# Factual Server API  Wrapper

This package wraps the Factual "Server" API. Its query style is SQLAlchemy-inspired and designed
to make it easy to build "read" requests by chaining filter calls together. 

API actions other than "read" are supported via the same syntax for consistency. 

You'll need to [get a Factual API key](http://www.factual.com/developers/api_key) (requires sign up).

## Usage

    from factual import *
    s = Session(api_key="deadbeef")
    my_place = s.read(tables.USPOI).search("coffee").run().records()[0]
    
You can also build requests one piece at a time:

	from factual.tables import USPOI,USLocalPlaypen
    query = s.read(USPOI)
    query.filter({"name": "Foobar"})
	if test_address != None:
		query.filter({"address": test_address})
    response = query.run()
    records = response.records()
    
Limiting categories and using the filter helper functions:

    from factual.filter_helpers import *
    q = s.read(USPOI).filter(or_(bw_("category", "Food"), bw_("category", "Arts")))
    q.search("Foobar")
    records = q.run().records()
    
Geo queries:

    coffee_places = s.read(USPOI).search("coffee").within(40.7353,-73.9912,1000).run().records()
    
Modify a record in the Playpen:

    p = s.read(USLocalPlaypen).search("coffee").count(1).run().records()[0]
    p['address'] += "/Foobar"
    s.input(USLocalPlaypen).values(p).comment("Silly update test").run()

See also the Python documentation for session.Session and requests.Read and [Factual's developer documentation](http://wiki.developer.factual.com/).

