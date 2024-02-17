import mysql.connector as mq

def get_all_data():
    query_to_get_all = f'select * from dataset';
    cur.execute(query_to_get_all)
    res = cur.fetchall()
    return res

def insert_new_data(lat, lng, cdate, edate, co, seurface_temp, precipitation, wind_direction, formal, ozone, popul, so2, evi, nvdi, ndwi, water_thick, Downward_Long_Wave_Radp_Flux_surface_6_Hour_Average, Downward_Short_Wave_Radiation_Flux_surface_6_Hour_Average, Geopotential_height_surface, Latent_heat_net_flux_surface_6_Hour_Average, Maximum_specific_humidity_at_2m_height_above_ground, Maximum_temperature_height_above_ground_6_Hour_Interval, Minimum_specific_humidity_at_2m_height_above_ground, Minimum_temperature_height_above_ground_6_Hour_Interval, Potential_Evaporation_Rate_surface_6_Hour_Average, Precipitation_rate_surface_6_Hour_Average, Pressure_surface, Sensible_heat_net_flux_surface_6_Hour_Average, Specific_humidity_height_above_ground, Temperature_height_above_ground, u_component_of_wind_height_above_ground, Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average, Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average, v_component_of_wind_height_above_ground, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150):
    query_to_insert = f'insert into dataset(LAT, LNG, CDATE, edate, CO, SURFACE_TEMP, PRECIPITATION, WIND_DIRECTION, FORMALDEHYDE, OZONE, POPULATION, SO2, EVI, NDVI, NDWI, WATER_THICKNESS, Downward_Long_Wave_Radp_Flux_surface_6_Hour_Average, Downward_Short_Wave_Radiation_Flux_surface_6_Hour_Average, Geopotential_height_surface, Latent_heat_net_flux_surface_6_Hour_Average, Maximum_specific_humidity_at_2m_height_above_ground, Maximum_temperature_height_above_ground_6_Hour_Interval, Minimum_specific_humidity_at_2m_height_above_ground, Minimum_temperature_height_above_ground_6_Hour_Interval, Potential_Evaporation_Rate_surface_6_Hour_Average, Precipitation_rate_surface_6_Hour_Average, Pressure_surface, Sensible_heat_net_flux_surface_6_Hour_Average, Specific_humidity_height_above_ground, Temperature_height_above_ground, u_component_of_wind_height_above_ground, Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average, Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average, v_component_of_wind_height_above_ground, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150) values ({lat}, {lng}, "{cdate}", "{edate}", {co}, {seurface_temp}, {precipitation}, "{wind_direction}", {formal}, {ozone}, {popul}, {so2}, {evi}, {nvdi}, {ndwi}, {water_thick}, {Downward_Long_Wave_Radp_Flux_surface_6_Hour_Average}, {Downward_Short_Wave_Radiation_Flux_surface_6_Hour_Average}, {Geopotential_height_surface}, {Latent_heat_net_flux_surface_6_Hour_Average}, {Maximum_specific_humidity_at_2m_height_above_ground}, {Maximum_temperature_height_above_ground_6_Hour_Interval}, {Minimum_specific_humidity_at_2m_height_above_ground}, {Minimum_temperature_height_above_ground_6_Hour_Interval}, {Potential_Evaporation_Rate_surface_6_Hour_Average}, {Precipitation_rate_surface_6_Hour_Average}, {Pressure_surface}, {Sensible_heat_net_flux_surface_6_Hour_Average}, {Specific_humidity_height_above_ground}, {Temperature_height_above_ground}, {u_component_of_wind_height_above_ground}, {Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average}, {Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average}, {v_component_of_wind_height_above_ground}, {Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm}, {Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm}, {Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm}, {Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150})'
    print(query_to_insert)
    cur.execute(query_to_insert)
    con.commit()

def create_table():
    try:
        query_create_table = 'CREATE TABLE DATASET(LAT DECIMAL(7, 4), LNG DECIMAL(7, 4), CDATE DATE, EDATE DATE, CO DOUBLE, SURFACE_TEMP DOUBLE, PRECIPITATION DOUBLE, WIND_DIRECTION VARCHAR(20), FORMALDEHYDE DOUBLE, OZONE DOUBLE, POPULATION DOUBLE, SO2 DOUBLE, EVI DOUBLE, NDVI DOUBLE, NDWI DOUBLE, WATER_THICKNESS DOUBLE, Downward_Long_Wave_Radp_Flux_surface_6_Hour_Average DOUBLE, Downward_Short_Wave_Radiation_Flux_surface_6_Hour_Average DOUBLE, Geopotential_height_surface DOUBLE, Latent_heat_net_flux_surface_6_Hour_Average DOUBLE, Maximum_specific_humidity_at_2m_height_above_ground DOUBLE, Maximum_temperature_height_above_ground_6_Hour_Interval DOUBLE, Minimum_specific_humidity_at_2m_height_above_ground DOUBLE, Minimum_temperature_height_above_ground_6_Hour_Interval DOUBLE, Potential_Evaporation_Rate_surface_6_Hour_Average DOUBLE, Precipitation_rate_surface_6_Hour_Average DOUBLE, Pressure_surface DOUBLE, Sensible_heat_net_flux_surface_6_Hour_Average DOUBLE, Specific_humidity_height_above_ground DOUBLE, Temperature_height_above_ground DOUBLE, u_component_of_wind_height_above_ground DOUBLE, Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average DOUBLE, Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average DOUBLE, v_component_of_wind_height_above_ground DOUBLE, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm DOUBLE, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm DOUBLE, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm DOUBLE, Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150 DOUBLE)'
        cur.execute(query_create_table)
        print('Created table sucessfully!')
        con.commit()
    except Exception as e:
        print('Error in table creation ' + e)

def create_database():
    try:
        query_create = 'CREATE DATABASE PROJNAME'
        cur.execute(query_create)
        con.commit()
    except:
        print('Error while creating deatabase')
    
def close():
    if con.is_connected():
        con.commit();
        con.close();
    else:
        return False
    
def connect():
    try:
        connection = mq.connect(host='localhost', user='root', password="root")
        print('Connnection Successfull!')
        return connection
    except:
        return False
    
def main():
    global con, cur
    con = connect()
    cur = con.cursor()
    try:
        cur.execute('use projname')
        print('Database exist already!')
    except:
        print('Database created successfully')
        create_database()
    cur.execute('use projname')
    cur.execute('SHOW tables')
    res = list(cur.fetchall()[0])
    if 'dataset' not in res:
        create_table()
    else:
        print('Table exist')
    # get_all()
    # insert_new_data(9.9252, 78.1198, '2024-02-01', '2024-02-10', 0.03518808195228991, 27.57631461266658, 0.0004811148392368863, "NorthEast", 3.435128124660247, 0.11072711178317367, 771.8509632783777, 0.0001466178056706792, -0.18097332676915553, -0.01190617369332947, -0.011113761041324879, -0.7361488938331604)
    
# main()