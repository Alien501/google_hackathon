import json

def get_co_level(co_amount):
    if co_amount == None:
        co_amount = 0
    SOURCE_CO = 'The presence of CO, SO2, and formaldehyde could indicate pollution from sources like traffic, industry'
    stat = ''
    if co_amount > 0.2:
        stat = 'high'
    elif co_amount >= 0.01 and co_amount <= 0.1:
        stat = 'normal'
    else:           # < 0.01
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }
    
def get_formaldehyde_level(fa_amount):
    if fa_amount == None:
        fa_amount = 0
    SOURCE_CO = 'Formaldehyde is a volatile organic compound that can be emitted from various sources, including combustion processes and certain industrial activities'
    stat = ''
    if fa_amount > 10:
        stat = 'high'
    elif fa_amount >= 0.5 and fa_amount <= 5:
        stat = 'normal'
    else:           # < 0.5
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }
    
def get_so_level(so_amount):
    if so_amount == None:
        so_amount = 0
    SOURCE_CO = 'Elevated SO2 levels may indicate industrial processes or combustion of sulfur-containing fuels, potentially contributing to air pollution'
    stat = ''
    if so_amount > 0.01:
        stat = 'high'
    elif so_amount >= 0.00005 and so_amount <= 0.002:
        stat = 'normal'
    else:           # < 0.00005
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }
    
def get_pop_level(po_amount):
    if po_amount == None:
        po_amount = 0
    SOURCE_CO = ''
    stat = ''
    if po_amount > 500:
        SOURCE_CO = ': Often results in increased demand for resources, infrastructure, and services, fostering economic opportunities but requiring careful management to address challenges like congestion, housing, and environmental impact'        
        stat = 'high'
    elif po_amount >= 50 and po_amount <= 500:
        SOURCE_CO = 'Strikes a balance between community resources and demand, supporting a mix of economic activities, infrastructure, and social services'        
        stat = 'normal'
    else:           # < 0.00005
        SOURCE_CO = ' Typically associated with more open spaces, lower resource demand, and potentially fewer economic opportunities; may lead to challenges in sustaining services and businesses'        
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }

def get_ozone_stat(oz_amount):
    if oz_amount == None:
        oz_amount = 0
    SOURCE_CO = ''
    stat = ''
    if oz_amount > 100:
        SOURCE_CO = 'Elevated ozone levels can pose health risks, especially for sensitive induviduals, and may indicate poorer air quality'        
        stat = 'high'
    elif oz_amount >= 50 and oz_amount <= 100:
        SOURCE_CO = 'These levels are within acceptable air quality standards and are generally safe for general population'        
        stat = 'normal'
    else:           # < 0.00005
        SOURCE_CO = ' Air quality is generally good and these levels are considered safe for general population'        
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }
    
def get_nvdi_veg(no_amount):
    if no_amount == None:
        no_amount = 0
    SOURCE_CO = ''
    stat = ''
    if no_amount > 0.5 and no_amount < 0.8:
        SOURCE_CO = 'Dense vegetation cover, including dense forests, croplands, and rainforests. Indicates areas with healthy and vigorous vegetation'        
        stat = 'high'
    elif no_amount >= 0.5 and no_amount < 0.2:
        SOURCE_CO = 'Moderate vegetation cover, including grasslands, shrublands, and sparse forests'
        stat = 'normal'
    else:           # < 0.00005
        SOURCE_CO = 'Sparse or no vegetation cover. Often associated with barren land, deserts, urban areas, or water bodies'        
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }

def get_ndwi_wat(no_amount):
    if no_amount == None:
        no_amount = 0
    SOURCE_CO = ''
    stat = ''
    if no_amount >= 0.2 and no_amount <= 1:
        SOURCE_CO = 'High water content, indicating areas with abundant water such as flooded areas, dense vegetation with high transpiration rates, or saturated soil conditions'        
        stat = 'high'
    elif no_amount >= -0.2 and no_amount < 0.2:
        SOURCE_CO = 'Moderate water content, including water bodies such as rivers, lakes, and wetlands. Also includes areas with some moisture in the soil or vegetation'
        stat = 'normal'
    else:           # < 0.00005
        SOURCE_CO = 'Low water content or absence of water. Typically found in non-vegetated areas such as barren land, deserts, or urban areas'        
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }
    
def get_Sensible_heat_net_flux_surface_6_Hour_Average(amount):
    if amount == None:
        amount = 0
    SOURCE_CO = 'Represents the average net flux of sensible heat at the Earth\'s surface over a 6-hour period. Higher values indicate increased heat transfer from the surface to the atmosphere, while lower values suggest reduced heat transfer'        
    stat = ''
    if amount >= 20:
        stat = 'high'
    elif amount >= 10 and amount < 20:
        stat = 'normal'
    else:           # < 0.00005
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }
    
def get_Specific_humidity_height_above_ground(amount):
    if amount == None:
        amount = 0
    SOURCE_CO = 'Represents the specific humidity (moisture content) at a certain height above the ground. Higher values indicate higher moisture content in the air, while lower values suggest drier condition'        
    stat = ''
    if amount >= 0.02:
        stat = 'high'
    elif amount >= 0.015 and amount < 0.02:
        stat = 'normal'
    else:           # < 0.00005
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }
    
def get_Temperature_height_above_ground(amount):
    if amount == None:
        amount = 0
    SOURCE_CO = 'Represents the temperature at a certain height above the ground. Higher values indicate warmer temperatures, while lower values suggest cooler temperatures'        
    stat = ''
    if amount >= 303:
        stat = 'high'
    elif amount >= 298 and amount < 303:
        stat = 'normal'
    else:           # < 0.00005
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }

def get_u_component_of_wind_height_above_ground(amount):
    if amount == None:
        amount = 0
    SOURCE_CO = 'Represents the east-west component of wind velocity at a certain height above the ground. Positive values indicate eastward wind flow, while negative values suggest westward wind flow'        
    stat = ''
    if amount > -1:
        stat = 'high'
    elif amount >= -3 and amount < -1:
        stat = 'normal'
    else:           # < 0.00005
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }

def get_Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average(amount):
    if amount == None:
        amount = 0
    SOURCE_CO = 'Represents the average upward long-wave radiation flux at the Earth\'s surface over a 6-hour period. Higher values indicate increased heat emitted from the Earth\'s surface, while lower values suggest reduced heat emission'        
    stat = ''
    if amount > 400:
        stat = 'high'
    elif amount >= 200 and amount < 400:
        stat = 'normal'
    else:           # < 0.00005
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }
    
def get_Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average(amount):
    if amount == None:
        amount = 0
    SOURCE_CO = 'Represents the average upward short-wave radiation flux at the Earth\'s surface over a 6-hour period. Higher values indicate increased sunlight reflected from the Earth\'s surface, while lower values suggest reduced sunlight reflection.'        
    stat = ''
    if amount > 20:
        stat = 'high'
    elif amount >= 10 and amount < 20:
        stat = 'normal'
    else:           # < 0.00005
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }
    
def get_v_component_of_wind_height_above_ground(amount):
    if amount == None:
        amount = 0
    SOURCE_CO = 'Represents the north-south component of wind velocity at a certain height above the ground. Positive values indicate northward wind flow, while negative values suggest southward wind flow'        
    stat = ''
    if amount > -1:
        stat = 'high'
    elif amount >= -3 and amount < -1:
        stat = 'normal'
    else:           # < 0.00005
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }

def get_Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm(amount):
    if amount == None:
        amount = 0
    SOURCE_CO = 'Represents the volumetric soil moisture content at a depth of 5cm below the surface layer. Higher values indicate higher soil moisture content, while lower values suggest drier soil conditions'        
    stat = ''
    if amount > 0.35:
        stat = 'high'
    elif amount >= .30 and amount < .35:
        stat = 'normal'
    else:           # < 0.00005
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }
    
def get_Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm(amount):
    if amount == None:
        amount = 0
    SOURCE_CO = 'Represents the volumetric soil moisture content at a depth of 25cm below the surface layer. Higher values indicate higher soil moisture content, while lower values suggest drier soil conditions.'        
    stat = ''
    if amount > 0.35:
        stat = 'high'
    elif amount >= .30 and amount < .35:
        stat = 'normal'
    else:           # < 0.00005
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }
    
def get_Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm(amount):
    if amount == None:
        amount = 0
    SOURCE_CO = 'Represents the volumetric soil moisture content at a depth of 70cm below the surface layer. : Higher values indicate higher soil moisture content, while lower values suggest drier soil conditions.'        
    stat = ''
    if amount > 0.35:
        stat = 'high'
    elif amount >= .30 and amount < .35:
        stat = 'normal'
    else:           # < 0.00005
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }
    
def get_Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150_cm(amount):
    if amount == None:
        amount = 0
    SOURCE_CO = 'Represents the volumetric soil moisture content at a depth of 150cm below the surface layer. Higher values indicate higher soil moisture content, while lower values suggest drier soil conditions'        
    stat = ''
    if amount > 0.35:
        stat = 'high'
    elif amount >= .30 and amount < .35:
        stat = 'normal'
    else:           # < 0.00005
        stat = 'low'
    return {
        'source': SOURCE_CO,
        'severity': stat
    }