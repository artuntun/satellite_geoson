from planet import api
client = api.ClientV1()
# I have picked some Silicon Valley, San Francisco, CA, USA, coordinates:
geojson_geometry = {
    "type": "Polygon",
    "coordinates": [
        [
            [
              -122.43576049804688,
              37.51299386065851
            ],
            [
              -122.34786987304686,
              37.155938651244625
            ],
            [
              -122.07595825195312,
              36.948794297566366
            ],
            [
              -121.8878173828125,
              37.18110808791507
            ],
            [
              -122.43576049804688,
              37.51299386065851
            ]
        ]
    ]
}
# get images that overlap with our area of interest
geometry_filter = {
    "type": "GeometryFilter",
    "field_name": "geometry",
    "config": geojson_geometry
}

# get images acquired within a date range
date_range_filter = {
    "type": "DateRangeFilter",
    "field_name": "acquired",
    "config": {
        "gte": "2018-08-31T00:00:00.000Z",
        "lte": "2018-09-01T00:00:00.000Z"
    }
}

#or you can pick any other times, wider timeframes, though it might contain a lot more data..
# only get images which have <50% cloud coverage
cloud_cover_filter = {
    "type": "RangeFilter",
    "field_name": "cloud_cover",
    "config": {
        "lte": 0.5
    }
}

# combine our geo, date, cloud filters
combined_filter = {
    "type": "AndFilter",
    "config": [geometry_filter, date_range_filter, cloud_cover_filter]
}

import os
import json
import requests
from requests.auth import HTTPBasicAuth

os.environ['PL_API_KEY']='ecc508079d684740a9d6ef942f200371'

# API Key stored as an env variable
PLANET_API_KEY = os.getenv('PL_API_KEY')

# will get a 4 band image with spectral data for Red, Green, Blue and Near-infrared values
item_type = "PSScene4Band"

# API request object
search_request = {
  "interval": "day",
  "item_types": [item_type],
  "filter": combined_filter
}

# fire off the POST request
search_result = requests.post(
    'https://api.planet.com/data/v1/quick-search',
    auth=HTTPBasicAuth(PLANET_API_KEY, ''),
    json=search_request
)

print(json.dumps(search_result.json(), indent=1))

# extract image IDs only
image_ids = [feature['id'] for feature in search_result.json()['features']]
print(image_ids)

# For demo purposes, just grab the first image ID
id0 = image_ids[0]
id0_url = 'https://api.planet.com/data/v1/item-types/{}/items/{}/assets'.format(item_type, id0)

# Returns JSON metadata for assets in this ID. Learn more: planet.com/docs/reference/data-api/items-assets/#asset
result = requests.get(
    id0_url,
    auth=HTTPBasicAuth(PLANET_API_KEY, '')
)

# List of asset types available for this particular satellite image
print(result.json().keys())

# This is "inactive" if the "analytic" asset has not yet been activated; otherwise 'active'
print(result.json()['analytic_dn']['status'])

# activate the asset for download:
links = result.json()[u"analytic_dn"]["_links"]
self_link = links["_self"]
activation_link = links["activate"]

# Request activation of the 'analytic' asset:
activate_result = requests.get(
    activation_link,
    auth=HTTPBasicAuth(PLANET_API_KEY, '')
)
activation_status_result = requests.get(
    self_link,
    auth=HTTPBasicAuth(PLANET_API_KEY, '')
)
download_link = activation_status_result.json()["location"]
print(download_link)
