
from factual.common.shared_filter_helpers import *

# geo ops
def within_(lat, lon, radius=1500):
	return {"$loc": {"$within": {"$center":[[ GeoScalar(lat), GeoScalar(lon)], radius]}}}

