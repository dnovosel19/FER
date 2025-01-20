import React ,{useEffect,useState} from 'react';
import './App.css';
import { Router } from './Router';
import { loadMapApi } from './utils/GoogleMapsUtils';

function App() {
  const [scriptLoaded,setScriptLoaded]=useState(false);
  useEffect(()=>{
    const googleMapScript=loadMapApi();
    googleMapScript.addEventListener('load',function(){
      setScriptLoaded(true);
    })
  },[]);
  return (
    <div className='app_container'>
      {scriptLoaded && (
        <Router/>
      )}
    </div>

  );
}

export default App;
