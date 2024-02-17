# import ee
# from datetime import datetime, timedelta

# # Initialize the Earth Engine API
# ee.Initialize()

# # Function to create a rectangular polygon around a point
# def create_polygon(latitude, longitude, buffer_size=1.0):
#     point = ee.Geometry.Point([longitude, latitude])
#     buffer_size_meters = ee.Number(buffer_size).multiply(1000)  # Convert buffer size from kilometers to meters
#     return point.buffer(buffer_size_meters).bounds()

# # Function to get average CO level for a given region
# def get_average_co_level(latitude, longitude, buffer_distance):
#     # Create a point for the user input location
#     point = ee.Geometry.Point(longitude, latitude)
    
#     # Create a rectangular buffer around the point
#     region = point.buffer(buffer_distance)
    
#     # Load the Sentinel-5P Carbon Monoxide dataset
#     s5p_co_dataset = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_CO")
    
#     # Specify the CO concentration band
#     co_band = "CO_column_number_density"
    
#     # Calculate the mean CO concentration
#     co_mean = (
#         s5p_co_dataset
#         .select(co_band)
#         .mean()
#     )
    
#     # Reduce the region to get the average value
#     co_value = co_mean.reduceRegion(
#         reducer=ee.Reducer.mean(),
#         geometry=region,
#         scale=1000  # Adjust scale as needed
#     )
    
#     return co_value.get(co_band)

# # Function to calculate average SO2 level for a given geometry and time range
# def calculate_so2_level(geometry, start_date, end_date):
#     # Load Sentinel-5P data
#     s5p_dataset = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_SO2') \
#         .filterBounds(geometry) \
#         .filterDate(ee.Date(start_date), ee.Date(end_date))

#     # Calculate the average SO2 level
#     so2_mean = s5p_dataset.select('SO2_column_number_density').mean()

#     # Reduce the region to get the mean value
#     so2_level = so2_mean.reduceRegion(
#         reducer=ee.Reducer.mean(),
#         geometry=geometry,
#         scale=1000  # Use an appropriate scale
#     )

#     return so2_level.get('SO2_column_number_density')

# # Function to get total population for a given region
# def get_total_population(latitude, longitude):
#     # Create a point for the given latitude and longitude
#     point = ee.Geometry.Point([longitude, latitude])
    
#     # Create a large rectangular polygon around the point
#     area_of_interest = point.buffer(100000)  # Buffer of 100 km around the point
    
#     # Load WorldPop population data
#     population_dataset = ee.ImageCollection("WorldPop/GP/100m/pop")
    
#     # Clip population data to the area of interest
#     population_clip = population_dataset.mean().clip(area_of_interest)

#     # Calculate the total population for the area of interest
#     total_population = population_clip.reduceRegion(
#         reducer=ee.Reducer.sum(),
#         geometry=area_of_interest,
#         scale=1000,  # 1 km resolution
#         maxPixels=1e13,
#         crs='EPSG:4326'  # Explicitly set the coordinate reference system
#     ).getInfo()['population']
    
#     return total_population

# # Function to retrieve formaldehyde level for a specified location
# def get_formaldehyde_level(latitude, longitude):
#     # Create a point for the specified location
#     location_point = ee.Geometry.Point([longitude, latitude])

#     # Load Sentinel-5P data
#     s5p_dataset = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2') \
#         .filterBounds(location_point)

#     # Select the band for formaldehyde
#     formaldehyde_band = 'tropospheric_NO2_column_number_density'

#     # Calculate the average formaldehyde level
#     formaldehyde_level = s5p_dataset.select([formaldehyde_band]) \
#         .mean() \
#         .reduceRegion(
#             reducer=ee.Reducer.mean(),
#             geometry=location_point,
#             scale=1000
#         )

#     return formaldehyde_level

# # Function to retrieve surface temperature, precipitation, and wind
# def get_era5_data(latitude, longitude, start_date, end_date):
#     # Create a point geometry for the location
#     point = ee.Geometry.Point([longitude, latitude])

#     # Define the ERA5 collection
#     era5_collection = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY').select(
#         ['temperature_2m', 'total_precipitation', 'u_component_of_wind_10m', 'v_component_of_wind_10m']
#     )

#     # Filter the collection based on location and time
#     filtered_era5 = era5_collection.filterBounds(point).filterDate(start_date, end_date)

#     # Get the mean values for each component
#     mean_values = filtered_era5.mean()

#     # Print the results
#     print("Temperature (2m):", mean_values.select('temperature_2m').reduceRegion(ee.Reducer.mean(), point).getInfo())
#     print("Total Precipitation:", mean_values.select('total_precipitation').reduceRegion(ee.Reducer.sum(), point).getInfo())
#     print("U Component of Wind (10m):", mean_values.select('u_component_of_wind_10m').reduceRegion(ee.Reducer.mean(), point).getInfo())
#     print("V Component of Wind (10m):", mean_values.select('v_component_of_wind_10m').reduceRegion(ee.Reducer.mean(), point).getInfo())

# # Main script
# if __name__ == "_main_":
#     # User input for latitude and longitude
#     latitude = float(input("Enter latitude: "))
#     longitude = float(input("Enter longitude: "))

#     # Create a rectangular polygon around the user-specified point
#     user_polygon = create_polygon(latitude, longitude, buffer_size=1.0)

#     # Call functions for different functionalities
#     co_level = get_average_co_level(latitude, longitude, buffer_distance=50000)
#     so2_level = calculate_so2_level(user_polygon, '2022-01-01', '2022-01-31')
#     population = get_total_population(latitude, longitude)
#     formaldehyde_level = get_formaldehyde_level(latitude, longitude)
    
#     # Specify the time range for ERA5 data
#     start_date_era5 = '2022-01-01'
#     end_date_era5 = '2022-01-10'
    
#     # Call the function to retrieve ERA5 data
#     get_era5_data(latitude, longitude, start_date_era5, end_date_era5)

#     # Print the results
#     print(f"Average CO Level: {co_level.getInfo()} µmol/m^2")
#     print(f"Average SO2 Level: {so2_level.getInfo() if so2_level.getInfo() is not None else 'No data available'}")
#     print(f"Total Population: {population}")
#     print(f"Formaldehyde Level: {formaldehyde_level.get('tropospheric_NO2_column_number_density').getInfo() if formaldehyde_level.get('tropospheric_NO2_column_number_density') is not None else 'No data available'}")
    
    
0 {'Downward_Long-Wave_Radp_Flux_surface_6_Hour_Average': 380.7780615355238}
1 {'Downward_Short-Wave_Radiation_Flux_surface_6_Hour_Average': 264.15729014783824}
2 {'Geopotential_height_surface': 19.98405622085723}
3 {'Latent_heat_net_flux_surface_6_Hour_Average': 49.24516265566988}
4 {'Maximum_specific_humidity_at_2m_height_above_ground_6_Hour_Interval': 0.01617671044192987}
5 {'Maximum_temperature_height_above_ground_6_Hour_Interval': 301.94392784798526}
6 {'Minimum_specific_humidity_at_2m_height_above_ground_6_Hour_Interval': 0.014703317381220295}
7 {'Minimum_temperature_height_above_ground_6_Hour_Interval': 296.6869391292158}
8 {'Potential_Evaporation_Rate_surface_6_Hour_Average': 365.7687965075806}
9 {'Precipitation_rate_surface_6_Hour_Average': 3.8682458773902273e-07}
10 {'Pressure_surface': 101307.53085860155}
11 {'Sensible_heat_net_flux_surface_6_Hour_Average': 104.50096985769746}
12 {'Specific_humidity_height_above_ground': 0.015317030292705147}
13 {'Temperature_height_above_ground': 299.24612217062787}
14 {'u-component_of_wind_height_above_ground': -2.2472844828001346}
15 {'Upward_Long-Wave_Radp_Flux_surface_6_Hour_Average': 458.37270494517736}
16 {'Upward_Short-Wave_Radiation_Flux_surface_6_Hour_Average': 27.876714280383432}
17 {'v-component_of_wind_height_above_ground': 0.9948098055915081}
18 {'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm': 0.21330718430552154}
19 {'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm': 0.2896226047938414}
20 {'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm': 0.3003443043951942}
21 {'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm': 0.309518354600019}


insert into dataset(LAT, LNG, CDATE, edate, CO, SURFACE_TEMP, PRECIPITATION, WIND_DIRECTION, FORMALDEHYDE, OZONE, POPULATION, SO2, EVI, NDVI, NDWI, WATER_THICKNESS, Downward_Long_Wave_Radp_Flux_surface_6_Hour_Average, Downward_Short_Wave_Radiation_Flux_surface_6_Hour_Average, Geopotential_height_surface, Latent_heat_net_flux_surface_6_Hour_Average, Maximum_specific_humidity_at_2m_height_above_ground, Maximum_temperature_height_above_ground_6_Hour_Interval, Minimum_specific_humidity_at_2m_height_above_ground, Minimum_temperature_height_above_ground_6_Hour_Interval, Potential_Evaporation_Rate_surface_6_Hour_Average, Precipitation_rate_surface_6_Hour_Average, Pressure_surface, Sensible_heat_net_flux_surface_6_Hour_Average, Specific_humidity_height_above_ground, Temperature_height_above_ground, u_component_of_wind_height_above_ground, Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average, Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average, v_component_of_wind_height_above_ground, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150) values (9.9252, 78.1198, "2024-02-01", "2024-02-15", 0.03518808195228991, 27.57631461266658, 27.57631461266658, "NorthEast", 3.434871899261902e-05, 0.11082803296906506, 771.8509632783777, 0.0001768287771101926, -0.18097332676915553, 0.01190617369332947, -0.011113761041324879, -0.7361488938331604, , 391.61609709576504, 263.39439243275143, 144.63891893758506, 72.4230193306973, 0.014303605588619124, 303.24101098246433, 0.013153413105037521, 297.882010397831, 300.6950888493177, 1.1464353002931449e-05, 99790.26487852374, 70.33601590693293, 0.013615595895343793, 300.44885090300636, -1.1909504414076388, 466.4119590268763, 38.267439767326266, -2.2606029078939196, 0.151399260738719, 0.17575242055099163, 0.18706898818089165, 0.2218960064042334)

Skipped data insertion due to  1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ', 391.61609709576504, 263.39439243275143, 144.63891893758506, 72.4230193306973, ' at line 1