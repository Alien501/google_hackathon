from flask import Flask, request
import ee
from datetime import datetime
import requests
import json
import math

import details
import db
import get_p

from flask_cors import CORS

app = Flask(__name__)
ee.Authenticate()
CORS(app)
db.main()
ee.Initialize(project='earth-engine-410402')


@app.route('/')
def main():
    return 'Hello World'

@app.route('/download')
def download():
    res = db.get_all_data()
    return {'data': res}   

# Function to create a rectangular polygon around a point
def create_polygon(latitude, longitude, buffer_size=1.0):
    point = ee.Geometry.Point(ee.List([longitude, latitude]))
    buffer_size_meters = ee.Number(buffer_size).multiply(1000)  # Convert buffer size from kilometers to meters
    return point.buffer(buffer_size_meters).bounds()

def get_new_data(latitude, longitude, start_date_in, end_date_in):
    poly = create_polygon(latitude, longitude)
    
    co = (get_average_co_level(region = poly))['res']
    co_stat = (details.get_co_level(co))
    so2 = (calculate_so2_level(start_date=start_date_in, end_date=end_date_in, geometry=poly))['res']
    so2_stat = (details.get_so_level(so2))
    pop = (get_total_population(area_of_interest=poly))['res']
    pop_stat = (details.get_pop_level(pop))
    formal = (get_formaldehyde_level(location_point = poly))['res']
    form_stat = (details.get_formaldehyde_level(formal))
    era5 = (get_era5_data( latitude=latitude, longitude=longitude, start_date=start_date_in, end_date=end_date_in, point1=poly))
    ozone = (get_ozone(user_polygon=poly, start_date=start_date_in, end_date=end_date_in))
    # print(ozone)
    ozone_stat = details.get_ozone_stat(ozone['res'])
    water = get_water(poly=poly)
    
    veg_data = get_veg(point=poly, start_date=start_date_in, end_date=end_date_in)
    soil_data = get_soil_data(latitude, longitude, start_date_in, end_date_in)
    
    try:
        veg_stat = details.get_nvdi_veg(veg_data['res']['NDVI Value'])
    except:
        veg_stat = None
    
    try:
        wat_stat = details.get_ndwi_wat(veg_data['res']['NDWI Value'])
    except:
        wat_stat = None
    
    try:
        if era5 == None:
            era5val1 = 0
            era5val2 = 0
            era5val3 = 0
        else:
            era5val1 = era5['res']['temperature']
            era5val2 = era5['res']['temperature']
            era5val3 = era5['res']['wind_direction']
        if veg_data == None:
            veg_val1 = 0
            veg_val2 = 0
            veg_val3 = 0
        else:
            veg_val1 = veg_data['res']['EVI Value']
            veg_val2 = veg_data['res']['NDVI Value']
            veg_val3 = veg_data['res']['NDWI Value']
        
        if water == None:
            water_val = 0
        else:
            water_val = water['res']['lwe_thickness_csr']
        
        db.insert_new_data(latitude, longitude, start_date_in, end_date_in, co, era5val1, era5val2, era5val3, formal, ozone['res'], pop, so2, veg_val1, veg_val2, veg_val3, water_val, soil_data['res'][0]['Downward_Long-Wave_Radp_Flux_surface_6_Hour_Average'], soil_data['res'][1]['Downward_Short-Wave_Radiation_Flux_surface_6_Hour_Average'],
        soil_data['res'][2]['Geopotential_height_surface'], soil_data['res'][3]['Latent_heat_net_flux_surface_6_Hour_Average'], soil_data['res'][4]['Maximum_specific_humidity_at_2m_height_above_ground_6_Hour_Interval'], soil_data['res'][5]['Maximum_temperature_height_above_ground_6_Hour_Interval'], soil_data['res'][6]['Minimum_specific_humidity_at_2m_height_above_ground_6_Hour_Interval'],
        soil_data['res'][7]['Minimum_temperature_height_above_ground_6_Hour_Interval'], soil_data['res'][8]['Potential_Evaporation_Rate_surface_6_Hour_Average'], soil_data['res'][9]['Precipitation_rate_surface_6_Hour_Average'],
        soil_data['res'][10]['Pressure_surface'], soil_data['res'][11]['Sensible_heat_net_flux_surface_6_Hour_Average'], soil_data['res'][12]['Specific_humidity_height_above_ground'], soil_data['res'][13]['Temperature_height_above_ground'], soil_data['res'][14]['u-component_of_wind_height_above_ground'], soil_data['res'][15]['Upward_Long-Wave_Radp_Flux_surface_6_Hour_Average'], soil_data['res'][16]['Upward_Short-Wave_Radiation_Flux_surface_6_Hour_Average'], soil_data['res'][17]['v-component_of_wind_height_above_ground'], soil_data['res'][18]['Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm'],
        soil_data['res'][19]['Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm'],
        soil_data['res'][20]['Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm'],
        soil_data['res'][21]['Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm'])
    except Exception as e:
        print('Skipped data insertion due to ', e)
    # print(soil_data['res'][0])
    try:
        Sensible_heat_net_flux_surface_6_Hour_Average_stat = details.get_Sensible_heat_net_flux_surface_6_Hour_Average(soil_data['res'][11]['Sensible_heat_net_flux_surface_6_Hour_Average'])
    except:
        Sensible_heat_net_flux_surface_6_Hour_Average_stat = 0
    try:
        Specific_humidity_height_above_ground_stat = details.get_Specific_humidity_height_above_ground(soil_data['res'][12]['Specific_humidity_height_above_ground'])
    except:
        Specific_humidity_height_above_ground_stat = 0
    try:
        Temperature_height_above_ground_stat = details.get_Temperature_height_above_ground(soil_data['res'][13]['Temperature_height_above_ground'])
    except:
        Temperature_height_above_ground_stat = 0
    try:
        u_component_of_wind_height_above_ground_stat = details.get_u_component_of_wind_height_above_ground(soil_data['res'][14]['u-component_of_wind_height_above_ground'])
    except:
        u_component_of_wind_height_above_ground_stat = 0
    try:
        Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average_stat = details.get_Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average(soil_data['res'][15]['Upward_Long-Wave_Radp_Flux_surface_6_Hour_Average'])
    except:
        Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average_stat = 0
    try:
        Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average_stat = details.get_Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average(soil_data['res'][16]['Upward_Short-Wave_Radiation_Flux_surface_6_Hour_Average'])
    except:
        Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average_stat = 0
    try:
        v_component_of_wind_height_above_ground_stat = details.get_v_component_of_wind_height_above_ground(soil_data['res'][17]['v-component_of_wind_height_above_ground'])
    except:
        v_component_of_wind_height_above_ground_stat = 0
    try:
        Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_stat = details.get_Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm(soil_data['res'][18]['Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm'])
    except:
        Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_stat = 0
    try:
        Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm_stat = details.get_Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm(soil_data['res'][19]['Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm'])
    except:
        Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm_stat = 0
    try:
        Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm_stat = details.get_Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm(soil_data['res'][20]['Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm'])
    except:
        Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm_stat = 0
    try:
        Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm_stat = details.get_Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm(soil_data['res'][21]['Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm'])
    except:
        Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm_stat = 0
    # print(soil_data)
    
    get_plant_details = get_p.get_plant_reccomendation(Temperature_height_above_ground_stat, Specific_humidity_height_above_ground_stat, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_stat, 'normal')
    
    return {
        'co': {'value': co, 'etc': co_stat},
        'so2': {'value': so2, 'etc': so2_stat},
        'population': {'value': pop, 'etc': pop_stat},
        'formaldehyde': {'value': formal, 'etc': form_stat},
        'era5': {'value': era5, 'etc': 'NA'},
        'ozone': {'value': ozone, 'etc': ozone_stat},
        'water': {'value': water},
        'vegetation': {
            'value': veg_data,
            'etc': {
                'NDVI': veg_stat,
                'NDWI': wat_stat
            }
        },
        'soil_data': {
            'value': soil_data,
            'etc': {
                'Sensible_heat_net_flux_surface_6_Hour_Average_stat': Sensible_heat_net_flux_surface_6_Hour_Average_stat,
                'Specific_humidity_height_above_ground_stat': Specific_humidity_height_above_ground_stat,
                'Temperature_height_above_ground_stat': Temperature_height_above_ground_stat,
                'u_component_of_wind_height_above_ground_stat': u_component_of_wind_height_above_ground_stat,
                'Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average_stat': Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average_stat,
                'Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average_stat': Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average_stat,
                'v_component_of_wind_height_above_ground_stat': v_component_of_wind_height_above_ground_stat,
                'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_stat': Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_stat,
                'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm_stat': Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm_stat,
                'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm_stat': Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm_stat,
                'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm_stat': Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm_stat
            }
        },
        'plant_data': get_plant_details
    }

@app.route('/getall')
def get_all():
    latitude = float(request.args.get('lat'))
    longitude = float(request.args.get('long'))
    start_date_in = str(datetime.strptime(request.args.get('std'), '%Y-%m-%d').date())
    end_date_in = str(datetime.strptime(request.args.get('end'), '%Y-%m-%d').date())
    
    result = db.get_all_data()
    
    if len(result) != 0:
        for i in result:
            if str(i[0]) == str(latitude) and str(i[1]) == str(longitude):
                print('found')
                print(i)
                co = i[3]
                sft = i[4]
                prec = i[5]
                wind_dir = i[6]
                formal = i[7]
                ozone = i[8]
                popl = i[9]
                so2 = i[10]
                evi = i[11]
                ndvi = i[12]
                ndwi = i[13]
                water = i[14]
                Downward_Long_Wave_Radp_Flux_surface_6_Hour_Average = i[16]
                Downward_Short_Wave_Radiation_Flux_surface_6_Hour_Average = i[17]
                Geopotential_height_surface = i[18]
                Latent_heat_net_flux_surface_6_Hour_Average = i[19]
                Maximum_specific_humidity_at_2m_height_above_ground = i[20]
                Maximum_temperature_height_above_ground_6_Hour_Interval = i[21]
                Minimum_specific_humidity_at_2m_height_above_ground = i[22]
                Minimum_temperature_height_above_ground_6_Hour_Interval = i[23]
                Potential_Evaporation_Rate_surface_6_Hour_Average = i[24]
                Precipitation_rate_surface_6_Hour_Average = i[25]
                Pressure_surface = i[26]
                
                Sensible_heat_net_flux_surface_6_Hour_Average_val = i[27]
                Specific_humidity_height_above_ground_val = i[28]
                Temperature_height_above_ground_val = i[29]
                u_component_of_wind_height_above_ground_val = i[30]
                Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average_val = i[31]
                Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average_val = i[32]
                v_component_of_wind_height_above_ground_val = i[33]
                Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_val = i[34]
                Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm_val = i[35]
                Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm_val = i[36]
                Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm_val = i[37]
                
                Sensible_heat_net_flux_surface_6_Hour_Average_stat = details.get_Sensible_heat_net_flux_surface_6_Hour_Average(Sensible_heat_net_flux_surface_6_Hour_Average_val)
                Specific_humidity_height_above_ground_stat = details.get_Specific_humidity_height_above_ground(Specific_humidity_height_above_ground_val)
                Temperature_height_above_ground_stat = details.get_Temperature_height_above_ground(Temperature_height_above_ground_val)
                u_component_of_wind_height_above_ground_stat = details.get_u_component_of_wind_height_above_ground(u_component_of_wind_height_above_ground_val)
                Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average_stat = details.get_Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average(Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average_val)
                Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average_stat = details.get_Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average(Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average_val)
                v_component_of_wind_height_above_ground_stat = details.get_v_component_of_wind_height_above_ground(v_component_of_wind_height_above_ground_val)
                Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_stat = details.get_Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm(Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_val)
                Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm_stat = details.get_Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm(Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm_val)
                Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm_stat = details.get_Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm(Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm_val)
                Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm_stat = details.get_Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm(Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm_val)

                co_stat = (details.get_co_level(co))
                so2_stat = (details.get_so_level(so2))
                pop_stat = (details.get_pop_level(popl))
                form_stat = (details.get_formaldehyde_level(formal))
                ozone_stat = details.get_ozone_stat(ozone)
                try:
                    veg_stat = details.get_nvdi_veg(ndvi)
                except:
                    veg_stat = None
                try:
                    wat_stat = details.get_ndwi_wat(ndwi)
                except:
                    wat_stat = None
                
                get_plant_details = get_p.get_plant_reccomendation(Temperature_height_above_ground_stat, Specific_humidity_height_above_ground_stat, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_stat, 'normal')
                
                return {
                    'co': {'value': co, 'etc': co_stat},
                    'so2': {'value': so2, 'etc': so2_stat},
                    'population': {'value': popl, 'etc': pop_stat},
                    'formaldehyde': {'value': formal, 'etc': form_stat},
                    'era5': {'value': {
                            'res': {
                                'temperature': sft,
                                "total_precipitation": prec,
                                "wind_direction": wind_dir
                            }
                        }, 'etc': 'NA'},
                    'ozone': {'value': ozone, 'etc': ozone_stat},
                    'water': {'value': {
                            'res': {
                                'lwe_thickness_csr': water
                            }
                        }},
                    'vegetation': {
                        'value': {
                                'res': {
                                    'EVI Value': evi,
                                    'NDVI Value': ndvi,
                                    'NDWI Value': ndwi
                                }
                            },
                        'etc': {
                            'NDVI': veg_stat,
                            'NDWI': wat_stat
                        }
                    },
                    'plant': get_plant_details,
                    'soil_data': {
                        'etc': {
                            'Sensible_heat_net_flux_surface_6_Hour_Average_stat': Sensible_heat_net_flux_surface_6_Hour_Average_stat,
                            'Specific_humidity_height_above_ground_stat': Specific_humidity_height_above_ground_stat,
                            'Temperature_height_above_ground_stat': Temperature_height_above_ground_stat,
                            'Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average_stat': Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average_stat,
                            'Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average_stat': Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average_stat,
                            'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm_stat': Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm_stat,
                            'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm_stat': Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm_stat,
                            'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_stat': Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_stat,
                            'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm_stat': Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm_stat,
                            'u_component_of_wind_height_above_ground_stat': u_component_of_wind_height_above_ground_stat,
                            'v_component_of_wind_height_above_ground_stat': v_component_of_wind_height_above_ground_stat
                        },
                        'value': {
                            'res': [
                                {
                                    'Downward_Long-Wave_Radp_Flux_surface_6_Hour_Average': Downward_Long_Wave_Radp_Flux_surface_6_Hour_Average
                                },
                                {
                                    'Downward_Short-Wave_Radiation_Flux_surface_6_Hour_Average': Downward_Short_Wave_Radiation_Flux_surface_6_Hour_Average
                                },
                                {
                                    'Geopotential_height_surface': Geopotential_height_surface
                                },
                                {
                                    'Latent_heat_net_flux_surface_6_Hour_Average': Latent_heat_net_flux_surface_6_Hour_Average
                                },
                                {
                                    'Maximum_specific_humidity_at_2m_height_above_ground_6_Hour_Interval': Maximum_specific_humidity_at_2m_height_above_ground
                                },
                                {
                                    'Maximum_temperature_height_above_ground_6_Hour_Interval': Maximum_temperature_height_above_ground_6_Hour_Interval
                                },
                                {
                                    'Minimum_specific_humidity_at_2m_height_above_ground_6_Hour_Interval': Minimum_specific_humidity_at_2m_height_above_ground
                                },
                                {
                                    'Minimum_temperature_height_above_ground_6_Hour_Interval': Minimum_temperature_height_above_ground_6_Hour_Interval
                                },
                                {
                                    'Potential_Evaporation_Rate_surface_6_Hour_Average': Potential_Evaporation_Rate_surface_6_Hour_Average
                                },
                                {
                                    'Precipitation_rate_surface_6_Hour_Average': Precipitation_rate_surface_6_Hour_Average
                                },
                                {
                                    'Pressure_surface': Pressure_surface
                                },
                                {
                                    'Sensible_heat_net_flux_surface_6_Hour_Average': Sensible_heat_net_flux_surface_6_Hour_Average_val
                                },
                                {
                                    'Specific_humidity_height_above_ground': Specific_humidity_height_above_ground_val
                                },
                                {
                                    'Temperature_height_above_ground': Temperature_height_above_ground_val
                                },
                                {
                                    'u-component_of_wind_height_above_ground': u_component_of_wind_height_above_ground_val
                                },
                                {
                                    'Upward_Long-Wave_Radp_Flux_surface_6_Hour_Average': Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average_val
                                },
                                {
                                    'Upward_Short-Wave_Radiation_Flux_surface_6_Hour_Average': Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average_val
                                },
                                {
                                    'v-component_of_wind_height_above_ground': v_component_of_wind_height_above_ground_val
                                },
                                {
                                    'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm': Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm_val
                                },
                                {
                                    'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm': Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm_val
                                },
                                {
                                    'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm': Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm_val
                                },
                                {
                                    'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm': Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm_val
                                }
                            ]
                        }
                    }
                }

    return get_new_data(latitude, longitude, start_date_in, end_date_in)

'''
co
st
pre
wd
forma
ozone
pop
so2
evi
ndvi
ndwi
water
'''

def get_average_co_level(region):
    
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
def calculate_so2_level(start_date, end_date, geometry):
    
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
def get_total_population(area_of_interest):

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
def get_formaldehyde_level(location_point):

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

    if 22.5 <= wind_direction_deg < 67.5:
        direction = "SouthWest"
    elif 67.5 <= wind_direction_deg < 112.5:
        direction = "West"
    elif 112.5 <= wind_direction_deg < 157.5:
        direction = "NorthWest"
    elif 157.5 <= wind_direction_deg < 202.5:
        direction = "North"
    elif 202.5 <= wind_direction_deg < 247.5:
        direction = "NorthEast"
    elif 247.5 <= wind_direction_deg < 292.5:
        direction = "East"
    elif 292.5 <= wind_direction_deg < 337.5:
        direction = "NorthEast"
    else:
        direction = "South"

    return direction

# Function to retrieve surface temperature, precipitation, and wind
def get_era5_data(latitude, longitude, start_date, end_date, point1):
    try:
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
        # print(mean_values)
        temp = mean_values.select('temperature_2m').reduceRegion(ee.Reducer.mean(), point).getInfo()['temperature_2m']
        total_precp = mean_values.select('total_precipitation').reduceRegion(ee.Reducer.sum(), point).getInfo()['total_precipitation']
        u_comp = mean_values.select('u_component_of_wind_10m').reduceRegion(ee.Reducer.mean(), point).getInfo()['u_component_of_wind_10m']
        v_comp = mean_values.select('v_component_of_wind_10m').reduceRegion(ee.Reducer.mean(), point).getInfo()['v_component_of_wind_10m']
        wind_dir = findWindDirection(u_comp, v_comp)
        
        return {
            'res': {
                'temperature': temp-273.15,
                'total_precipitation': total_precp,
                'wind_direction': wind_dir
            }
        }
        
    except:
        return None

    
def get_ozone(user_polygon, start_date, end_date):


    s5p_ozone_dataset = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_O3') \
        .filterBounds(user_polygon) \
        .filterDate(ee.Date(start_date), ee.Date(end_date))
    first_image = s5p_ozone_dataset.first()
    band_names = first_image.bandNames()

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


def calculate_vegetation_indices(image):
    # Calculate NDVI
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

    # Calculate NDWI
    ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')

    # Calculate EVI
    evi = image.expression(
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
            'NIR': image.select('B8'),
            'RED': image.select('B4'),
            'BLUE': image.select('B2')
        }).rename('EVI')

    return ndvi.addBands(ndwi).addBands(evi)

def get_veg(point, start_date, end_date):

    sentinel2 = ee.ImageCollection('COPERNICUS/S2') \
        .filterBounds(point) \
        .filterDate(start_date, end_date) \
        .first()  # Select the first image in the collection

    # Calculate vegetation indices
    vegetation_indices_image = calculate_vegetation_indices(sentinel2)

    # Extract values at the point of interest
    vegetation_indices_values = vegetation_indices_image.reduceRegion(reducer=ee.Reducer.mean(), geometry=point, scale=10)
    try:
        val1 = vegetation_indices_values.get('NDVI').getInfo()
        val2 = vegetation_indices_values.get('NDWI').getInfo()
        val3 = vegetation_indices_values.get('EVI').getInfo()
    except:
        return None
    return {
        'res': {
            "NDVI Value": val1,
            "NDWI Value": val2,
            "EVI Value": val3 
        }
    }
    
    
def get_soil_data(lat, lon, start_date, end_date):
    try:
        dataset = ee.ImageCollection('NOAA/CFSV2/FOR6H')
        first_image = dataset.first()
        band_names = first_image.bandNames().getInfo()

        buffer_radius = 0.1  # Adjust this radius as needed
        region_of_interest = ee.Geometry.Rectangle([lon - buffer_radius, lat - buffer_radius, lon + buffer_radius, lat + buffer_radius])

        # Filter the dataset by date and location
        filtered_dataset = dataset.filterDate(start_date, end_date)\
                                .filterBounds(region_of_interest)

        datas = []
        # Iterate over each band
        for band_name in band_names:
            # Get the values for the band
            band_values = filtered_dataset.select(band_name)\
                                        .mean()\
                                        .reduceRegion(ee.Reducer.mean(), region_of_interest, 5000)\
                                        .get(band_name)\
                                        .getInfo()
            
            a = {band_name: band_values}
            datas.append(a)
        return {
            'res': datas
        }
    except:
        return None