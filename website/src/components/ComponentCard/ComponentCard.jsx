import React from "react";

import './ComponentCard.css';

export default function ComponentCard({compName}) {
    return(
        <div className="component-card-container">
            <p className="component-name">
                {compName}
            </p>
        </div>
    )
}