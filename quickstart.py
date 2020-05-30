import os
import json
import argparse
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date

api = SentinelAPI('artuntun', 'h48n4zqwe!', 'https://scihub.copernicus.eu/dhus')

# pass the input-file and date
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("-i", "--input", help="Input coordinates",
                    default='./california.json')
parser.add_argument("-ds", "--date-start", help="dates to search thru",
                    default='20190719')
parser.add_argument("-de", "--date-end", help="dates to search thru",
                    default='20190729')

args = parser.parse_args()
# download single scene by known product id
# api.download('c23ccf2b-a133-48b4-8389-1778972893dc')

# search by polygon, time, and SciHub query keywords
footprint = geojson_to_wkt(read_geojson(args.input))
products = api.query(footprint,
                     date=(args.date_start, args.date_end),
                     platformname='Sentinel-2',
                     cloudcoverpercentage=(0, 30))

with open('output.geojson', 'w') as fp:
    json_products = api.to_geojson(products)
    json.dump(json_products, fp)

os.system('geojsonio output.geojson')

# # download all results from the search
# api.download_all(products)

# # convert to Pandas DataFrame
# products_df = api.to_dataframe(products)

# # GeoJSON FeatureCollection containing footprints and metadata of the scenes
# api.to_geojson(products)

# # GeoPandas GeoDataFrame with the metadata of the scenes and the footprints as geometries
# api.to_geodataframe(products)

# # Get basic information about the product: its title, file size, MD5 sum, date, footprint and
# # its download url
# api.get_product_odata('S2B_MSIL2A_20191103T075009_N0213_R135_T38SLF_20191103T095700')

# # Get the product's full metadata available on the server
# api.get_product_odata('S2B_MSIL2A_20191103T075009_N0213_R135_T38SLF_20191103T095700', full=True)
