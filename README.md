# Factual Server API  Wrapper

This package wraps the [Factual v3 API][factual_docs]. Its query style is SQLAlchemy-inspired and designed
to make it easy to build "read" requests by chaining filter calls together. 

There is also limited support for v2 API, including actions other than "read," under the "v2" subpackage.

Note that there are minor API inconsistencies between the v2 and v3 versions, both on the server side 
and in this wrapper. The v3 version of the wrapper is now the default.

## API access

To get started, you'll need to [register for Factual API OAuth credentials][factual_signup]. 

## Usage

First, create a Session using your v3 API OAuth consumer key and consumer secret:

    import factual
	session = factual.Session(
                             consumer_key="myOAuthConsumerKey",
                             consumer_secret="myOAuthConsumerSecret"
                             )

Now, build a query using the <tt>read</tt> action on the <tt>"global"</tt> table:

    query = session.read("global")

You can apply as many filters as you'd like to the query. Filters on a query are cumulative, and can be chained:

    query.search("coffee")
	query.filter({"locality": "Albany"}).filter({"region":"NY"})

When you're done, <tt>run()</tt> the query and retrieve the results using the <tt>records()</tt> method:

	from pprint import pprint
    
    data = query.run().records()
	pprint(data)

### Geographic queries

You probably want to search for places near a point. Use the <tt>within(latitude, longitude, radius_in_meters)</tt> 
helper method of <tt>read</tt>.  <tt>within()</tt> chains and applies like any other filter, except that the
last call will overwrite earlier geo filters.  The underlying Factual filter API has changed between v2 and v3, but 
this will work for both:

    query = session.read("global").within(40.7353,-73.9912,1000).search("coffee")

### Pagination

Get more results using <tt>count()</tt> and <tt>page()</tt>: 

    query.count(30).page(2) # 30 results per request, second page of results

Note that Factual's API instead uses <tt>limit</tt> and <tt>offset</tt>, so I should probably change the wrapper to match.

### Categories

Factual provides categories as hierarchical strings. That is, any place marked "Food & Beverage > Bakeries" 
is in the "Bakeries" subcategory of "Food & Beverage." 

It's possible to query for either specific subcategories or parent categories using the <tt>$bw</tt> 
("begins with") filter operator.  You can then search across multiple of these <tt>$bw</tt> filters by 
chaining them together with <tt>$or</tt>.

Because this can get pretty lengthy, the <tt>category_helpers</tt> module has a <tt>make_category_filter</tt> function. 
<tt>make_category_filter</tt> takes a list of category strings and combines them into a <tt>$bw</tt>/<tt>or</tt> filter.
Since <tt>$bw</tt> will always include all subcategories of an supercategory listed, <tt>make_category_filter</tt> also
dedupes the provided categories to generate the shortest list possible. This may mean that it will include more 
subcategories than you indended; but if you want to get in to <tt>$and $not $bw</tt> tangles, you're on your own. 

Pass <tt>blank = True</tt> as a kwarg to <tt>make_category_filter</tt> if you also want results without categories set.

    from factual import category_helpers

	my_categories = [ "Food & Beverage", "Food & Beverage > Bakeries", "Shopping" ]
	my_filters = category_helpers.make_category_filter(my_categories, blank=True)
    # {'$or': ({'category': {'$bw': 'Food & Beverage'}}, {'category': {'$bw': 'Shopping'}}, {'category': {'$blank': True}})}

	query = s.read("global").filter(my_filters)

### Non-OAuth requests

It's possible to skip OAuth for the v3 API, if, for instance, there's some trouble with 
signing requests. Creating a Session without a <tt>consumer_secret</tt> will authenticate
requests via the <tt>KEY</tt> query string parameter rather than OAuth:

    non_oauth_session = factual.Session(consumer_key="myOAuthConsumerKey")

Note that Factual [discourages falling back to the <tt>KEY</tt> parameter][factual_requests_KEY], 
and intends it for debugging use only, so use OAuth if possible.

## Examples

    from factual import *
    s = Session(consumer_key="deadbeef", consumer_secret="foobar")
    my_place = s.read("global").search("coffee").run().records()[0]
    
Building requests one piece at a time:

    query = s.read("global")
	query.filter({"name": "Foobar"})
    if my_address != None:
        query.filter({"address": my_address})
    response = query.run()
    records = response.records()
    
Limiting categories and using the filter helper functions:

    from factual.filter_helpers import *
    q = s.read("global").filter(
                        or_(
                            bw_("category", "Food"), 
                            bw_("category", "Arts")
                        )
                      ).search("Foobar")
    records = q.run().records()
    
Geo queries:

    # lat, lon, radius in meters
    coffee_places = s.read(places).search("coffee").within(40.7353,-73.9912,1000).run().records()

## Factual v2 "Server" API

To use the v2 API, instantiate a factual.v2.Session object instead of a factual.Session object:

    import factual
    v2_session = factual.v2.Session(api_key="deadbeef")
	...

Note that you'll need to provide a v2 API key using the <tt>api_key</tt> argument. Factual
issues v2 API keys via a different process than for v3 API credentials. 
    
In the v2 API, you can also modify a record in the Playpen:

	v2_session = factual.v2.Session(api_key="deadbeef")
    p = v2_session.read(USLocalPlaypen).search("coffee").count(1).run().records()[0]
    p['address'] += "/Foobar"
    v2_session.input(USLocalPlaypen).values(p).comment("Silly update test").run()

See also the Python documentation for session.Session and requests.Read and [Factual's developer documentation][factual_docs].

## TODO

- Write support for v3, when available
- Multiple search filters (search filters currently replace one another)

## Changelog

- v0.1.2 - Add async option to Request.run() to permit delaying the processing of the HTTP response.
           If the asynchttp module is installed, this will cause the initial call to run(async=True)
		   to immediately return a get_response function, allowing you to defer the blocking 
		   call until the results are needed. 

[factual_docs]: http://developer.factual.com/display/docs/Factual+Developer+APIs+Version+3
[factual_requests_KEY]: http://developer.factual.com/display/docs/Core+API+-+Oauth#CoreAPI-Oauth-KeysandSecrets
[factual_signup]: https://www.factual.com/api-keys/request
