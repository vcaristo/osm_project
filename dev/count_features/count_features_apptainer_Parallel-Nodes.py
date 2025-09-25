import geopandas as gpd
from pathlib import Path
import pandas as pd
import sys


state = sys.argv[1]

# apptainer paths
base = Path('/mnt/osm_project/')
state_path = base / "data" / state
output_path = base / "dev" / "count_features" / "output-parallel" / f"features_count_{state}.out"

# setup output file
layers = ['parks', 'pitches', 'sports_centres', 'schools']
result = pd.DataFrame(columns = ['state', 'county'] + layers)


files = [f for f in state_path.iterdir() if f.is_file()] # full file paths

for county_gpk_path in files:
    county_name = county_gpk_path.name.split(".gpkg")[0]
    
    # initial county data record
    county_data = {'state':state, 'county':county_name}
    
    for layer in layers:
        try:
            gdf = gpd.read_file(county_gpk_path, layer=layer)
            county_data[layer] = len(gdf)
        except:         # in case layer doesn't exist
            county_data[layer] = 0

    # add county data to result
    result.loc[len(result)] = county_data

result.to_csv(output_path, index=False)