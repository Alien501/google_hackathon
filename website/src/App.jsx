import { useState } from 'react'

import './App.css'
import TopNavBar from './components/TopNavBar/TopNavBar'
import Explainer from './components/Explainer/Explainer'
import PrimaryButton from './components/PrimaryButton/PrimaryButton'

function App() {

  async function onDownloadClick(event) {
    try {
      const res = await fetch('http://172.16.66.233:8080/download')
      const data = await res.json()
      data['data'].unshift(['LAT', 'LNG', 'CDATE', 'CO', 'SURFACE_TEMP', 'PRECIPITATION', 'WIND_DIRECTION', 'FORMALDEHYDE', 'OZONE', 'POPULATION', 'SO2', 'EVI', 'NDVI', 'NDWI', 'WATER_THICKNESS', 'edate', 'Downward_Long_Wave_Radp_Flux_surface_6_Hour_Average', 'Downward_Short_Wave_Radiation_Flux_surface_6_Hour_Average', 'Geopotential_height_surface', 'Latent_heat_net_flux_surface_6_Hour_Average', 'Maximum_specific_humidity_at_2m_height_above_ground', 'Maximum_temperature_height_above_ground_6_Hour_Interval', 'Minimum_specific_humidity_at_2m_height_above_ground', 'Minimum_temperature_height_above_ground_6_Hour_Interval', 'Potential_Evaporation_Rate_surface_6_Hour_Average', 'Precipitation_rate_surface_6_Hour_Average', 'Pressure_surface', 'Sensible_heat_net_flux_surface_6_Hour_Average', 'Specific_humidity_height_above_ground', 'Temperature_height_above_ground', 'u_component_of_wind_height_above_ground', 'Upward_Long_Wave_Radp_Flux_surface_6_Hour_Average', 'Upward_Short_Wave_Radiation_Flux_surface_6_Hour_Average', 'v_component_of_wind_height_above_ground', 'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_5_cm', 'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_25_cm','Volumetric_Soil_Moisture_Content_depth_below_surface_layer_70_cm', 'Volumetric_Soil_Moisture_Content_depth_below_surface_layer_150'])
      const csvContent = data['data'].map(row => row.join(',')).join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'data.csv';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <>
      <TopNavBar />
      <Explainer />
      <div className="download-btn-container">
        <PrimaryButton btnName={'DOWNLOAD'} btnFunction={onDownloadClick} />
      </div>
    </>
  )
}

export default App
