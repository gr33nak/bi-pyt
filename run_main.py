"""
    Flood risk score application

    Description:
    This script serves as the main entry point for your application.
    It handles the execution of the main logic or functions.

    Author:
    Ondřej Zelený

    Date:
    Date Created: [01 07, 2024]

    Usage:
    By default, this script can be executed by running the following command:
    $ python3 run_main.py
    It will ask you for an adress and then it will print the risk score of the adress.
"""

# Import necessary libraries
import numpy as np
import geopandas as gpd

# import all functions
from functions import *

# Load geojson files
rivers = gpd.read_file("rivers.geojson")
water_bodies = gpd.read_file("water_bodies.geojson")
border = gpd.read_file("border.geojson")
border = border.drop('NAZ_STAT', axis=1)
forests = gpd.read_file("forests.geojson")
regions = gpd.read_file("regions.geojson")

# Set quantiles for rivers, water bodies and forests plus region specific precipitation scores for each month
"""
    Those were calculated in the jupyter notebook. The calculation is time consuming so I decided to do it only once.
    The jupyter notebook is in the repository in case you want to see the calculation.
"""
proximity_quantiles_rivers = np.array([0.00101484, 0.00205205, 0.00315813, 0.00433401, 0.00559006, 0.00698083,
 0.00862364, 0.01077285, 0.01405417])

proximity_quantiles_water_bodies = np.array([0.01058209, 0.01950404, 0.02715884, 0.0355059, 0.04431191, 0.05452197,
0.06668492, 0.08311381, 0.10878065])

forest_quantiles = np.array([ 0., 0., 5.18138845, 15.32095872, 26.25553836, 37.97792867,
 52.57936547, 70.03155797, 92.7178144])

precipitation_scores = {
    'Jihomoravský kraj': [1, 1, 1, 1, 1, 1, 5, 4, 6, 1, 1, 1],
    'Jihočeský kraj': [5, 2, 2, 5, 10, 10, 10, 9, 1, 2, 5, 2],
    'Karlovarský kraj': [10, 8, 9, 7, 3, 2, 4, 6, 8, 7, 9, 10],
    'Královéhradecký kraj': [9, 7, 8, 6, 5, 5, 3, 1, 2, 8, 10, 8],
    'Liberecký kraj': [10, 10, 10, 9, 5, 9, 9, 3, 5, 10, 10, 10],
    'Moravskoslezský kraj': [4, 9, 9, 10, 10, 10, 10, 10, 10, 10, 6, 7],
    'Olomoucký kraj': [2, 6, 6, 8, 4, 4, 7, 7, 9, 6, 3, 6],
    'Pardubický kraj': [3, 5, 7, 4, 7, 5, 5, 5, 7, 5, 4, 5],
    'Plzeňský kraj': [5, 5, 5, 5, 5, 7, 2, 8, 3, 3, 7, 5],
    'Praha a Středočeský kraj': [1, 1, 1, 2, 2, 8, 1, 1, 1, 1, 1, 1],
    'Kraj Vysočina': [6, 3, 4, 1, 8, 5, 6, 5, 5, 4, 5, 4],
    'Zlínský kraj': [8, 10, 5, 10, 9, 1, 8, 10, 10, 9, 8, 9],
    'Ústecký kraj': [7, 4, 3, 3, 1, 3, 1, 2, 4, 5, 2, 3]
}

# set score weights
score_weights = {
    'elevation': 0.3,
    'rivers': 0.3,
    'water_bodies': 0.1,
    'forest': 0.1,
    'month_weights': [0.0125, 0.025, 0.025, 0.025, 0.0125, 0.025, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125]
}

# main function
if __name__ == "__main__":
    while True:
        # Get address from user
        address = input("Enter address: ")

        # Get coordinates from address
        coordinates = get_coordinates(address)

        # Check if coordinates are valid
        if coordinates:
            if is_not_within_border(coordinates, border):
                print("Address is not within Czechia. Please enter a valid address.")
            else:
                break  # Exit the loop if coordinates are valid
        else:
            print("Invalid address. Please enter a valid address.")

    # Get elevation from coordinates
    elevation = get_elevation_from_coordinates(coordinates)

    # Get elevation score
    elevation_score = elevation_to_decile(elevation)

    # Get proximity to rivers
    proximity_rivers = distance_to_nearest_object(coordinates, rivers)

    # Get score for proximity to rivers
    rivers_score = proximity_to_score(proximity_rivers, proximity_quantiles_rivers)

    # Get proximity to water bodies
    proximity_water_bodies = distance_to_nearest_object(coordinates, water_bodies)

    # Get score for proximity to water bodies
    water_bodies_score = proximity_to_score(proximity_water_bodies, proximity_quantiles_water_bodies)

    # Get proximity to forests
    forested_area = forested_area_percentage(coordinates, forests)

    # Get score for percentage of forested area
    forest_score = forest_percentage_to_score(forested_area, forest_quantiles)

    # Get proximity to border
    region_name = get_region_name(coordinates, regions)

    # Get precipitation score
    precipitation_score = precipitation_scores[region_name]

    # Calculate risk score
    risk_score = calculate_risk_score(elevation_score, rivers_score, water_bodies_score, forest_score, precipitation_score, score_weights)

    # Print risk score
    print(f"Flood risk score for {address} is {risk_score}.")
