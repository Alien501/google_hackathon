import json

def get_co_level(co_amount):
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