import React from "react";


import './Explainer.css';
import ComponentCard from "../ComponentCard/ComponentCard";

export default function Explainer() {
    return(
        <div className="explainer-container">
            <h1>Datasets we Provide</h1>
            <div className="explainer-card-container">
                <ComponentCard compName='Latitude'/>
                <ComponentCard compName='Longtitude'/>
                <ComponentCard compName='Date Range'/>
                <ComponentCard compName='CO'/>
                <ComponentCard compName='Formaldehyde'/>
                <ComponentCard compName='SO2'/>
                <ComponentCard compName='Ozone'/>
                <ComponentCard compName='Vegetation Data'/>
                <ComponentCard compName='Water Thickness'/>
                <ComponentCard compName='Soil Moisture'/>
                <ComponentCard compName='Wind Components'/>
                <ComponentCard compName='Humidity'/>
                <ComponentCard compName='Surface Temperature'/>
                <ComponentCard compName='And so on...'/>
            </div>
        </div>
    )
}