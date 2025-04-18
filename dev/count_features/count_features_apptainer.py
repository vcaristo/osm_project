import geopandas as gpd
from pathlib import Path
import pandas as pd

# apptainer path 
base = Path('/mnt/osm_project/data')

# setup output file
layers = ['parks', 'pitches', 'sports_centres', 'schools']
result = pd.DataFrame(columns = ['state', 'county'] + layers)

# list all the state folders
states = [f.name for f in base.iterdir() if f.is_dir()]

for state in states:
    state_path = base / state

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

result.to_csv(base / "features_count_2025-04-09.csv")