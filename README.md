# Flood Risk Assessment Tool

The Flood Risk Assessment Tool for Czechia is a Python project that assesses the risk level of a given location in Czechia based on various factors.

## Introduction

The Flood Risk Assessment Tool aims to provide users with a risk score for a given adress in Czechia. This score is calculated based on factors such as elevation, proximity to rivers, water bodies, forests, and precipitation.

## Installation

To install the project dependencies, run the following command:

pip install -r requirements.txt

## Usage

Run the main script run_main.py, input an address and get the risk assessment:

python run_main.py

From you adress the application takes corresponding coordinates based on geopy.geocoders.
Examples: Národní 1, Praha, Czechia || Národní 1, Prague || Prague

## Dependencies

The project relies on the following Python libraries:

- [numpy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [geopy](https://geopy.readthedocs.io/)
- [geopandas](https://geopandas.org/)
- [rasterio](https://rasterio.readthedocs.io/)
- [shapely](https://shapely.readthedocs.io/)
