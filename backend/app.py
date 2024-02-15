from flask import Flask, request
import ee
from datetime import datetime
import requests
import json
import math

import details

app = Flask(__name__)
ee.Authenticate()

ee.Initialize(project='earth-engine-410402')


@app.route('/')
def main():
    return 'Hello World'

# Function to create a rectangular polygon around a point
def create_polygon(latitude, longitude, buffer_size=1.0):
    point = ee.Geometry.Point(ee.List([longitude, latitude]))
    buffer_size_meters = ee.Number(buffer_size).multiply(1000)  # Convert buffer size from kilometers to meters
    return point.buffer(buffer_size_meters).bounds()

@app.route('/getall')
def get_all():
    latitude = float(request.args.get('lat'))
    longitude = float(request.args.get('long'))
    start_date_in = str(datetime.strptime(request.args.get('std'), '%Y/%m/%d').date())
    end_date_in = str(datetime.strptime(request.args.get('end'), '%Y/%m/%d').date())
    
    print('Start Date: ', str(start_date_in))
    print('End Date: ', str(end_date_in))
    
    poly = create_polygon(latitude, longitude)
    
    co = (get_average_co_level(latitude, longitude, buffer_distance=5000, region = poly))['res']
    co_stat = (details.get_co_level(co))
    so2 = (calculate_so2_level( latitude=latitude, longitude=longitude, start_date=start_date_in, end_date=end_date_in, geometry=poly))['res']
    so2_stat = (details.get_so_level(so2))
    pop = (get_total_population(latitude, longitude, area_of_interest=poly))['res']
    pop_stat = (details.get_pop_level(pop))
    formal = (get_formaldehyde_level(latitude, longitude, location_point = poly))['res']
    form_stat = (details.get_formaldehyde_level(formal))
    era5 = (get_era5_data( latitude=latitude, longitude=longitude, start_date=start_date_in, end_date=end_date_in, point1=poly))
    ozone = (get_ozone(latitude, longitude, user_polygon=poly, start_date=start_date_in, end_date=end_date_in))
    # print(ozone)
    ozone_stat = details.get_ozone_stat(ozone['res'])
    water = get_water(poly=poly)
    
    return {
        'co': {'value': co, 'etc': co_stat},
        'so2': {'value': so2, 'etc': so2_stat},
        'population': {'value': pop, 'etc': pop_stat},
        'formaldehyde': {'value': formal, 'etc': form_stat},
        'era5': {'value': era5, 'etc': 'NA'},
        'ozone': {'value': ozone, 'etc': ozone_stat},
        'water': {'value': water}
    }
    

def get_average_co_level(latitude, longitude, buffer_distance, region):
    # # Create a point for the user input location
    # point = ee.Geometry.Point(ee.List([longitude, latitude]))
    
    # # Create a rectangular buffer around the point
    # region = point.buffer(buffer_distance)
    
    # Load the Sentinel-5P Carbon Monoxide dataset
    s5p_co_dataset = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_CO")
    
    # Specify the CO concentration band
    co_band = "CO_column_number_density"
    
    # Calculate the mean CO concentration
    co_mean = (
        s5p_co_dataset
        .select(co_band)
        .mean()
    )
    
    # Reduce the region to get the average value
    co_value = co_mean.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=1000  # Adjust scale as needed
    ).getInfo()
    
    return {'res': co_value[co_band]}

# Function to calculate average SO2 level for a given geometry and time range
def calculate_so2_level(latitude, longitude, start_date, end_date, geometry):
    
    s5p_dataset = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_SO2') \
        .filterBounds(geometry) \
        .filterDate(ee.Date(start_date), ee.Date(end_date))

    # Calculate the average SO2 level
    so2_mean = s5p_dataset.select('SO2_column_number_density').mean()

    # Reduce the region to get the mean value
    so2_level = so2_mean.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry,
        scale=1000  # Use an appropriate scale
    ).getInfo()

    return {'res': so2_level.get('SO2_column_number_density')}

# Function to get total population for a given region
def get_total_population(latitude, longitude, area_of_interest):
    # Create a point for the given latitude and longitude
    # point = ee.Geometry.Point(ee.List([longitude, latitude]))
    
    # # Create a large rectangular polygon around the point
    # area_of_interest = point.buffer(100000)  # Buffer of 100 km around the point
    
    # Load WorldPop population data
    population_dataset = ee.ImageCollection("WorldPop/GP/100m/pop")
    
    # Clip population data to the area of interest
    population_clip = population_dataset.mean().clip(area_of_interest)

    # Calculate the total population for the area of interest
    total_population = population_clip.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=area_of_interest,
        scale=1000,  # 1 km resolution
        maxPixels=1e13,
        crs='EPSG:4326'  # Explicitly set the coordinate reference system
    ).getInfo()['population']
    
    return {'res': total_population}

# Function to retrieve formaldehyde level for a specified location
def get_formaldehyde_level(latitude, longitude, location_point):
    # Create a point for the specified location
    # location_point = ee.Geometry.Point(ee.List([longitude, latitude]))

    # Load Sentinel-5P data
    s5p_dataset = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2') \
        .filterBounds(location_point)

    # Select the band for formaldehyde
    formaldehyde_band = 'tropospheric_NO2_column_number_density'

    # Calculate the average formaldehyde level
    formaldehyde_level = s5p_dataset.select([formaldehyde_band]) \
        .mean() \
        .reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=location_point,
            scale=1000
        ).getInfo()

    return {'res': formaldehyde_level[formaldehyde_band]}

def findWindDirection(u_component, v_component):
    wind_direction_rad = math.atan2(v_component, u_component)
    wind_direction_deg = math.degrees(wind_direction_rad)
    wind_direction_deg = (wind_direction_deg + 360) % 360

    if 45 <= wind_direction_deg < 135:
        direction = "East"
    elif 135 <= wind_direction_deg < 225:
        direction = "South"
    elif 225 <= wind_direction_deg < 315:
        direction = "West"
    else:
        direction = "North"

    return direction

# Function to retrieve surface temperature, precipitation, and wind
def get_era5_data(latitude, longitude, start_date, end_date, point1):
    # Create a point geometry for the location
    point = ee.Geometry.Point(ee.List([longitude, latitude]))

    # Define the ERA5 collection
    era5_collection = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY').select(
        ['temperature_2m', 'total_precipitation', 'u_component_of_wind_10m', 'v_component_of_wind_10m']
    )

    # Filter the collection based on location and time
    filtered_era5 = era5_collection.filterBounds(point).filterDate(start_date, end_date)

    # Get the mean values for each component
    mean_values = filtered_era5.mean()
    temp = mean_values.select('temperature_2m').reduceRegion(ee.Reducer.mean(), point).getInfo()['temperature_2m']
    total_precp = mean_values.select('total_precipitation').reduceRegion(ee.Reducer.sum(), point).getInfo()['total_precipitation']
    u_comp = mean_values.select('u_component_of_wind_10m').reduceRegion(ee.Reducer.mean(), point).getInfo()['u_component_of_wind_10m']
    v_comp = mean_values.select('v_component_of_wind_10m').reduceRegion(ee.Reducer.mean(), point).getInfo()['v_component_of_wind_10m']
    wind_dir = findWindDirection(u_comp, v_comp)
    
    return {
        'res': {
            'temperature': temp,
            'total_precipitation': total_precp,
            'wind_direction': wind_dir
        }
    }

    
def get_ozone(latitude, longitude, user_polygon, start_date, end_date):
    # user_polygon = create_polygon(latitude, longitude, buffer_size=1.0)
    # start_date = '2022-01-01'
    # end_date = '2022-01-31'

    s5p_ozone_dataset = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_O3') \
        .filterBounds(user_polygon) \
        .filterDate(ee.Date(start_date), ee.Date(end_date))
    first_image = s5p_ozone_dataset.first()
    band_names = first_image.bandNames()
    # print("Available band names:", band_names.getInfo())

    mean_ozone_image = s5p_ozone_dataset.mean()

    reduction_band_name = 'O3_column_number_density'
    average_ozone = mean_ozone_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=user_polygon,
        scale=1000  # Adjust scale as needed
    )
    ozone_value = average_ozone.get(reduction_band_name)

    if ozone_value is not None:
        # return {'status': True, 'ozone': ozone_value.getInfo()}
        return {'res': ozone_value.getInfo()}
    else:
        # return {'status': False, 'ozone': 'Na'}
        return None

def get_water(poly):
    # point = ee.Geometry.Point(lon, lat)

    grace_dataset = ee.ImageCollection("NASA/GRACE/MASS_GRIDS/LAND") \
        .filterBounds(poly) \
        .select('lwe_thickness_csr') 
    vis_params = {
        'min': -50,  # minimum value for visualization
        'max': 50,   # maximum value for visualization
        'palette': ['blue', 'white', 'red']  # color palette
    }

    mean_value = grace_dataset.mean().reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=poly,
        scale=5000  # Resolution in meters
    ).getInfo()

    return {'res': mean_value}