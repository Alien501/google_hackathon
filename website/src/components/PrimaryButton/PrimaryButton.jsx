import React from "react";

import './PrimaryButton.css';

export default function PrimaryButton({btnName, btnFunction}) {
    return(
        <button className="primary-button" onClick={btnFunction}>
            {btnName}
        </button>
    )
}