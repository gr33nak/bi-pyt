"""
    This moduse contains tests for functions.py
"""

import pytest
import numpy as np
from functions import *
import geopandas as gpd

# GPD data for testing
water_bodies = gpd.read_file("water_bodies.geojson")
border = gpd.read_file("border.geojson")
border = border.drop('NAZ_STAT', axis=1)
forests = gpd.read_file("forests.geojson")
regions = gpd.read_file("regions.geojson")

# Mock data for testing
test_coordinates = (15.417, 50.073)
test_forest_percentage = 35.730323288632206

# Test elevation_to_decile function
def test_elevation_to_decile_score():
    """
    Test the logic of elevation scores.
    """
    assert elevation_to_decile(300) > elevation_to_decile(800)

# Test get_elevation_from_coordinates function
def test_get_elevation_from_coordinates():
    """
    Test the type of elevation value.
    """
    assert isinstance(get_elevation_from_coordinates(test_coordinates), np.float32)

# Test get_coordinates function
def test_get_coordinates():
    """
    Test type of coordinates returned.
    """
    assert isinstance(get_coordinates("Prague, Czechia"), tuple)

# Test proximity_to_score function
def test_proximity_to_score():
    """
    Test the output of proximity_to_score function.
    """
    assert proximity_to_score(0.005, np.array([0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009])) == 5

# Test distance_to_nearest_object function
def test_distance_to_nearest_object():
    """
    Test the type of distance returned.
    """
    assert isinstance(distance_to_nearest_object(test_coordinates, water_bodies), float)

# Test forested_area_percentage function
def test_forested_area_percentage():
    """
    Test the output of forested_area_percentage function for specific coordinates.
    """
    assert forested_area_percentage(test_coordinates, forests) == test_forest_percentage

# Test forest_percentage_to_score function
def test_forest_percentage_to_score():
    """
    Test the logic of forest scores.
    """
    assert forest_percentage_to_score(test_forest_percentage, np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])) == 7

# Test get_region_name function
def test_get_region_name():
    """
    Test the ourput of get_region_name function for specific coordinates.
    """
    assert get_region_name(test_coordinates, regions) == 'Pardubický kraj'

# Test is_not_within_border function
def test_is_not_within_border():
    """
    Test the functionality of is_not_within_border function.
    """
    assert is_not_within_border(test_coordinates, border) is False

# Test calculate_risk_score function
def test_calculate_risk_score():
    """
    Test the output type of risk calculation function.
    """
    assert isinstance(
        calculate_risk_score(5, 8, 7, 6, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2], {'elevation': 0.3, 'rivers': 0.3, 'water_bodies': 0.1, 'forest': 0.1, 'month_weights': [0.0125, 0.025, 0.025, 0.025, 0.0125, 0.025, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125, 0.0125]}),
        float
    )
