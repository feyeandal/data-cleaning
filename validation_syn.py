import pandas as pd
import csv
import json
import jsonschema
from jsonschema import validate, ValidationError, SchemaError

# Schema based from the PhilAWARE data model
bldgSchema = {
    "type": "object",
    "properties": {
        "building": {"type": "string", "enum": ["house", "residential"]},
        "floor:material": {"type": "string", "enum": ["ground", "wood", "cement", "ceramics", "concrete"]},
        "addr:street": {"type": "string"},
        "addr:city": {"type": "string"},
        "building:levels": {"type": "number"},
        "building:material": {"type": "string", "enum": ["concrete", "brick", "masonry", "bamboo", "plaster", "cement_block", "wood", "glass_reinforced_plastic", "glass", "CI_sheet", "steel", "aluminum", "mixed"]},
        "roof:material": {"type": "string", "enum": ["concrete", "roof_tiles", "metal", "steel", "eternit", "thatch", "tile", "wood", "asbestos", "no_roof"]},
    },
    "required": ["building", "floor:material","addr:street","addr:city","building:levels","building:material","roof:material"]
}

def validateJson(data):
    try:
        validate(instance=data, schema=bldgSchema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

with open('residential_building.geojson', 'r', encoding="utf8") as f:
    data = json.load(f)

# Get all features read
features = data['features']

# Adding the id and status in the list
id = []
status = []

# Iterate over the data validating the properties field
for feature in features:
    isValid = validateJson(feature['properties'])
    if isValid:
        id.append(feature['id'])
        status.append("valid")
    else:
        id.append(feature['id'])
        status.append("invalid")
    print ("validating data...")

print ("validation done. check output file.")

df = pd.DataFrame(data={"node_num": id, "stat_node": status})
df.to_csv("./output45.csv", sep=',', index=False)