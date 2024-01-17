import ee
from datetime import datetime, timedelta

# Initialize the Earth Engine API
ee.Initialize()

# Function to create a rectangular polygon around a point
def create_polygon(latitude, longitude, buffer_size=1.0):
    point = ee.Geometry.Point([longitude, latitude])
    buffer_size_meters = ee.Number(buffer_size).multiply(1000)  # Convert buffer size from kilometers to meters
    return point.buffer(buffer_size_meters).bounds()

# Function to get average CO level for a given region
def get_average_co_level(latitude, longitude, buffer_distance):
    # Create a point for the user input location
    point = ee.Geometry.Point(longitude, latitude)
    
    # Create a rectangular buffer around the point
    region = point.buffer(buffer_distance)
    
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
    )
    
    return co_value.get(co_band)

# Function to calculate average SO2 level for a given geometry and time range
def calculate_so2_level(geometry, start_date, end_date):
    # Load Sentinel-5P data
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
    )

    return so2_level.get('SO2_column_number_density')

# Function to get total population for a given region
def get_total_population(latitude, longitude):
    # Create a point for the given latitude and longitude
    point = ee.Geometry.Point([longitude, latitude])
    
    # Create a large rectangular polygon around the point
    area_of_interest = point.buffer(100000)  # Buffer of 100 km around the point
    
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
    
    return total_population

# Function to retrieve formaldehyde level for a specified location
def get_formaldehyde_level(latitude, longitude):
    # Create a point for the specified location
    location_point = ee.Geometry.Point([longitude, latitude])

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
        )

    return formaldehyde_level

# Function to retrieve surface temperature, precipitation, and wind
def get_era5_data(latitude, longitude, start_date, end_date):
    # Create a point geometry for the location
    point = ee.Geometry.Point([longitude, latitude])

    # Define the ERA5 collection
    era5_collection = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY').select(
        ['temperature_2m', 'total_precipitation', 'u_component_of_wind_10m', 'v_component_of_wind_10m']
    )

    # Filter the collection based on location and time
    filtered_era5 = era5_collection.filterBounds(point).filterDate(start_date, end_date)

    # Get the mean values for each component
    mean_values = filtered_era5.mean()

    # Print the results
    print("Temperature (2m):", mean_values.select('temperature_2m').reduceRegion(ee.Reducer.mean(), point).getInfo())
    print("Total Precipitation:", mean_values.select('total_precipitation').reduceRegion(ee.Reducer.sum(), point).getInfo())
    print("U Component of Wind (10m):", mean_values.select('u_component_of_wind_10m').reduceRegion(ee.Reducer.mean(), point).getInfo())
    print("V Component of Wind (10m):", mean_values.select('v_component_of_wind_10m').reduceRegion(ee.Reducer.mean(), point).getInfo())

# Main script
if __name__ == "_main_":
    # User input for latitude and longitude
    latitude = float(input("Enter latitude: "))
    longitude = float(input("Enter longitude: "))

    # Create a rectangular polygon around the user-specified point
    user_polygon = create_polygon(latitude, longitude, buffer_size=1.0)

    # Call functions for different functionalities
    co_level = get_average_co_level(latitude, longitude, buffer_distance=50000)
    so2_level = calculate_so2_level(user_polygon, '2022-01-01', '2022-01-31')
    population = get_total_population(latitude, longitude)
    formaldehyde_level = get_formaldehyde_level(latitude, longitude)
    
    # Specify the time range for ERA5 data
    start_date_era5 = '2022-01-01'
    end_date_era5 = '2022-01-10'
    
    # Call the function to retrieve ERA5 data
    get_era5_data(latitude, longitude, start_date_era5, end_date_era5)

    # Print the results
    print(f"Average CO Level: {co_level.getInfo()} µmol/m^2")
    print(f"Average SO2 Level: {so2_level.getInfo() if so2_level.getInfo() is not None else 'No data available'}")
    print(f"Total Population: {population}")
    print(f"Formaldehyde Level: {formaldehyde_level.get('tropospheric_NO2_column_number_density').getInfo() if formaldehyde_level.get('tropospheric_NO2_column_number_density') is not None else 'No data available'}")