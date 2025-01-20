import React from 'react'
import '../styles/MainP.css'
import Footera from './FooterC'
import MapComponent from './Marker'

import { Link } from 'react-router-dom'
import { Button } from '@mui/material'
import { NavigateNext } from '@mui/icons-material'
import EmailIcon from '@mui/icons-material/Email';
import CallIcon from '@mui/icons-material/Call';

type Props = {}

const MainP = (props: Props) => {
  return (
    <div className='container'>
        <div className='header'>
            {/* <Link to="/login"><button className='button_header' id='button_login'>Log In </button></Link>
            <Link to="/register"><button className='button_header' id='button_register'>Register </button></Link> */}
              <div className = "item">&nbsp; &nbsp;
                Please <Link to="/login"><Button className = "btn" variant='outlined' sx={{color: 'black', borderColor: 'transparent', bgcolor: '', '&:hover': {bgcolor: 'red', color: 'white'}}}><b>LOGIN</b></Button></Link>
                or <Link to="/register"><Button className = "btn" variant='outlined' sx={{color: 'black', borderColor: 'transparent', bgcolor: '', '&:hover': {bgcolor: 'red', color: 'white'}}}><b>REGISTER</b></Button></Link>
              </div>
              <div className='cont' title='Contact Us'><EmailIcon sx={{ml: '30px'}}/>&nbsp;mili@vili.hr&nbsp;&nbsp;&nbsp;&nbsp;<CallIcon/>&nbsp;+385 (0)1 2345 678</div>
        </div>
        {/* <div className='karta'>
            <Map mapType={google.maps.MapTypeId.ROADMAP} mapTypeControl={true} />
            <div className='za_izbrisati'>kontrola mape,dio2</div>
        </div> */}
        <MapComponent/>
        <div className='raspored'>
          <Link to="/schedule"><Button variant="outlined" startIcon={<NavigateNext/>} sx={{borderRadius: '20px', overflow: 'hidden', color: 'white', bgcolor: 'red', '&:hover': { bgcolor: '', borderColor: 'red', color: 'black', '& svg': {visibility: 'visible'} } }}>Schedule</Button></Link>
        </div>
        {/* <Footera />                  */}
    </div>
  )
}

export default MainP