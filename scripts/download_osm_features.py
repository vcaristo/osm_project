import osmnx as ox
import pandas as pd
import numpy as np
import os

os.makedirs("gpkg", exist_ok=True)

us_states = [
    "Alabama, USA", "Alaska, USA", "Arizona, USA", "Arkansas, USA",
    "California, USA", "Colorado, USA", "Connecticut, USA", "Delaware, USA",
    "Florida, USA", "Georgia, USA", "Hawaii, USA", "Idaho, USA",
    "Illinois, USA", "Indiana, USA", "Iowa, USA", "Kansas, USA",
    "Kentucky, USA", "Louisiana, USA", "Maine, USA", "Maryland, USA",
    "Massachusetts, USA", "Michigan, USA", "Minnesota, USA", "Mississippi, USA",
    "Missouri, USA", "Montana, USA", "Nebraska, USA", "Nevada, USA",
    "New Hampshire, USA", "New Jersey, USA", "New Mexico, USA", "New York, USA",
    "North Carolina, USA", "North Dakota, USA", "Ohio, USA", "Oklahoma, USA",
    "Oregon, USA", "Pennsylvania, USA", "Rhode Island, USA", "South Carolina, USA",
    "South Dakota, USA", "Tennessee, USA", "Texas, USA", "Utah, USA",
    "Vermont, USA", "Virginia, USA", "Washington, USA", "West Virginia, USA",
    "Wisconsin, USA", "Wyoming, USA"
]

tags = {"leisure":["pitch", "park", "sports_centre"], 
        'building':'school', 
        'amenity':'school'}

for state in us_states:
    try:
        gdf = ox.features.features_from_place(state, tags)
        out_file = f"gpkg/{state.split(',')[0].lower().replace(' ', '_')}.gpkg"
        gdf.to_file(out_file, driver="GPKG")
    except Exception as e:
        with open("errors.log", 'a') as log:
            log.write(f"Error writing {state}")
