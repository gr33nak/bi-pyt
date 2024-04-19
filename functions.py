"""
Description:
    This file contains necessary functions for my application.
    These functions serve specific purposes and are used in the main script.

"""
# Import necessary libraries
import numpy as np
from geopy.geocoders import Nominatim
import rasterio
from shapely.geometry import Point
from shapely.ops import nearest_points

# Load tiff file
with rasterio.open("czech_elevation.tif") as elevation_src:
    czech_elevation = elevation_src.read(1)

# Import necessary functions
# Get elevation deciles
def elevation_to_decile(elevation):
    """
    Get elevation deciles

    Parameters:
        elevation (float): Elevation in meters
    
    Returns:
        score (int): Score 1-10 based on elevation decile
    """
    # Flatten and remove NaN values
    elevation_values = czech_elevation.flatten()
    elevation_values = elevation_values[~np.isnan(elevation_values)]

    # Calculate deciles
    deciles = np.percentile(elevation_values, [10, 20, 30, 40, 50, 60, 70, 80, 90])
    # Assign the elevation to the appropriate decile bin
    score = 10 - np.digitize(elevation, deciles)

    return score

# Get elevation from coordinates
def get_elevation_from_coordinates(coordinates):
    """
    Get elevation from raster file at specified coordinates.

    Parameters:
    - coordinates (tuple): Tuple of (longitude, latitude) coordinates.

    Returns:
    - float: Elevation value at the specified coordinates.
    """
    with rasterio.open("czech_elevation.tif") as src:
        # Read the raster data
        elevation = src.read(1)

        # Convert coordinates to pixel indices using the affine transformation
        col, row = ~src.transform * coordinates

        # Round to the nearest integer (pixel indices should be integers)
        col, row = int(round(col)), int(round(row))

        # Extract elevation value
        elevation_value = elevation[row, col]

        return elevation_value

# Get coordintes from address
def get_coordinates(address):
    """
    Get geographic coordinates (latitude and longitude) from an address.

    Parameters:
    - address (str): The address to geocode.

    Returns:
    - tuple: A tuple containing the latitude and longitude.
    """
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address)
    if location:
        return location.longitude, location.latitude
    return None

# Get proximity score
def proximity_to_score(proximity, quantiles):
    """
    Get proximity score based on previously defined quantile values.

    Parameters:
    - proximity (float): Proximity to the nearest object of interest.

    Returns:
    - score (int): Score 1-10 based on proximity decile.
    """
    # Assign the proximity value to the appropriate quantile bin
    score = 10 - np.digitize(proximity, quantiles)

    return score

# Get proximity to nearest object
def distance_to_nearest_object(coordinates, water):
    """
    Calculate the distance from a pair of coordinates to the nearest river.

    Parameters:
        coordinates (tuple): Pair of coordinates as (longitude, latitude).
        water (GeoDataFrame): GeoDataFrame representing object of interest.

    Returns:
        distance (float): Distance from the coordinates to the nearest object of interest (in degrees).
    """
    # Create a Shapely Point geometry from the coordinates
    point = Point(coordinates)

    # Find the nearest river geometry using Shapely's nearest_points function
    nearest_river = nearest_points(point, water.unary_union)[1]

    # Calculate the distance using the distance method
    distance = point.distance(nearest_river)

    return distance

# Get percentage of forest in proximity
def forested_area_percentage(coordinates, forests, buffer_radius = 0.01):
    """
    Calculate the percentage of forested area in a circular buffer around the coordinates.

    Parameters:
        coordinates (tuple): Pair of coordinates as (longitude, latitude).
        forests (GeoDataFrame): GeoDataFrame representing forest polygons.
        buffer_radius (float): Radius of the circular buffer in degrees.

    Returns:
        percentage (float): Percentage of forested area in the buffer.
    """
    # Create a Shapely Point geometry from the coordinates
    point = Point(coordinates)

    # Create a circular buffer around the point
    buffer_zone = point.buffer(buffer_radius)

    # Calculate the intersection of the buffer zone with the forest polygons
    intersection = forests.intersection(buffer_zone)

    # Calculate the total area of the buffer zone
    total_buffer_area = buffer_zone.area

    # Calculate the total area of the forested region within the buffer
    forested_area = intersection.area.sum()

    # Calculate the percentage of forested area in the buffer
    percentage = (forested_area / total_buffer_area) * 100

    return percentage

# Get forest quantile score
def forest_percentage_to_score(percentage, quantiles):
    """
    Get percentage score based on previously defined quantile values.

    Parameters:
    - percentage (float): Percentage of forested area.

    Returns:
    - score (int): Score 1-10 based on percentage decile.
    """
    # Assign the percentage value to the appropriate quantile bin
    score = 10 - np.digitize(percentage, quantiles)

    return score

# Get region name from coordinates
def get_region_name(coordinates, region):
    """
    Get region name from given coordinates.

    Parameters:
    - coordinates (tuple): Pair of coordinates as (longitude, latitude).
    - region (GeoDataFrame): GeoDataFrame representing regions.

    Returns:
    - region name (str): Name of the region.
    """
    point = Point(coordinates)

    for index, row in region.iterrows():
        if point.within(row['geometry']):
            if row['NAZ_CZNUTS3'] == 'Hlavní město Praha' or row['NAZ_CZNUTS3'] == 'Středočeský kraj':
                return 'Praha a Středočeský kraj'
            return row['NAZ_CZNUTS3']  # Assuming 'NAZ_CZNUTS3' contains the region names

    return None  # Return None if the point is not within any region

# Check if coordinates are in Czechia
def is_not_within_border(coordinates, border):
    """
    Check if coordinates are within the Czechia border.

    Parameters:
    - coordinates (tuple): Pair of coordinates as (longitude, latitude).
    - border (GeoDataFrame): GeoDataFrame representing the Czechia border.

    Returns:
    - bool: True if coordinates are not within the Czechia border, False otherwise.
    """
    def is_within_border():
        point = Point(coordinates)
        return point.within(border['geometry'].iloc[0])
    return not is_within_border()

# Calculate final flood risk score
def calculate_risk_score(elevation_score, rivers_score, water_bodies_score, forest_score, precipitation_score, score_weights):
    """
    Calculate a risk score based on various environmental factors.

    Parameters:
    - elevation_score (float): Score based on elevation (1-10).
    - rivers_score (float): Score based on proximity to rivers (1-10).
    - water_bodies_score (float): Score based on proximity to water bodies (1-10).
    - forest_score (float): Score based on percentage of forested area (1-10).
    - precipitation_score (list): Monthly scores based on precipitation for the region.
    - score_weights (dict): Weights for different factors and months.
    
    Returns:
    - float: Normalized risk score between 1 and 10.
    """
    # Calculate the weighted average of scores
    weighted_average = (
        elevation_score * score_weights['elevation'] +
        rivers_score * score_weights['rivers'] +
        water_bodies_score * score_weights['water_bodies'] +
        forest_score * score_weights['forest'] +
        sum(score * weight for score, weight in zip(precipitation_score, score_weights['month_weights']))
    )

    return weighted_average
