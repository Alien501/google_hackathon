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
