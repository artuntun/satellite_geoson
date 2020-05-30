import os
import requests

item_id = "20160707_195147_1057916_RapidEye-1"
item_type = "REOrthoTile"
asset_type = "visual"

# setup auth
os.environ['PL_API_KEY']='ecc508079d684740a9d6ef942f200371'
session = requests.Session()
session.auth = (os.environ['PL_API_KEY'], '')

# request an item
item = \
  session.get(
    ("https://api.planet.com/data/v1/item-types/" +
    "{}/items/{}/assets/").format(item_type, item_id))

# extract the activation url from the item for the desired asset
item_activation_url = item.json()[asset_type]["_links"]["activate"]

# request activation
response = session.post(item_activation_url)

print(response.status_code)
