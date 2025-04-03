import osmnx as ox
import pandas as pd
import time
import requests
import os
from pathlib import Path
from datetime import datetime

# primary input / output parameters
counties_df = pd.read_csv('../us_counties.csv')
download_path = Path(f"../data")
results_df = pd.DataFrame(columns = ['state', 'name_full', 'name_abbrev', 'downloaded', 'file_path', 'size', 'date'])

# parse the county name
def get_abbrev_name(county_row):
    county = county_row['name_full'].split(",")[0]

    # remove 'County' suffix
    suffix_loc = county.find("County")

    if suffix_loc != -1:
        county = county[:suffix_loc].strip()
    
    return county

# OSM parameters
tags = {"leisure":["pitch", "park", "sports_centre"], 
        'building':'school', 
        'amenity':'school'}

states = counties_df['state'].unique()

for state in states:
    # create state folder
    state_path = download_path / state
    os.makedirs(state_path, exist_ok=True)

    for _, county_row in counties_df[counties_df['state'] == state].iterrows():

        county_full = county_row['name_full']
        county_abbrev = get_abbrev_name(county_row).replace(".","").replace(" ", "_")
        file_path = state_path / f"{county_abbrev}.gpkg"

        try:
            # call to OSMnX 
            features_gdf = ox.features.features_from_place(county_full, tags)

            # separate features
            parks = features_gdf[features_gdf['leisure'] == 'park']
            pitches = features_gdf[features_gdf['leisure'] == 'pitch']
            sports_centres = features_gdf[features_gdf['leisure'] == 'sports_centre']
            schools = features_gdf[features_gdf.apply(lambda x: True if "school" in [str(x['amenity']).lower(), str(x['building']).lower(), str(x['name']).lower()] else False, axis=1)] 

            # write geopackage to disk
            for gdf_obj, layer_name in [(parks, "parks"), (pitches, "pitches"), 
                            (sports_centres, "sports_centres"), (schools, "schools")]:

                # drop FID column (it's sepcial if GeoPackages, and not needed)
                if 'FID' in gdf_obj.columns:
                    gdf_obj = gdf_obj.drop(columns=['FID'])

                # save as layer in a GeoPackage
                gdf_obj.to_file(file_path, layer=layer_name, driver="GPKG")

            # get file size (decimal, not binary)
            size_kb = file_path.stat().st_size / 1000
            size_text = f"{size_kb} KB" if size_kb < 1000 else f"{size_kb / 1000:0.1f} MB"

            downloaded = 'Success'

            print(f"Success: {county_full}")

        except:
            downloaded = 'Fail'
            file_path = size_text = ''

            print(f"Fail: {county_full}")
        finally:
            date = datetime.today().strftime('%Y-%m-%d')
            
            # save results 
            results_data = {'state':state, 'name_full':county_full, 'name_abbrev':county_abbrev,
                             'downloaded':downloaded, 'file_path':file_path, 'size':size_text, 'date':date}
            
            results_df.loc[len(results_df)] = results_data

# date for file names
todays_date = datetime.strftime(datetime.now(), '%Y-%m-%d')

results_df.to_csv(download_path / f"results_{todays_date}.csv", index=False)