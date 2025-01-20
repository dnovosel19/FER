import React from 'react'
import '../styles/Footer.css'

type Props = {}

const FooterC = (props: Props) => {
  
     return (
    <div className='footer'>
        <div className='footer_logos'>
            {/*<img src={require('../materials/HZZO.png')} className='slike_footer'/>
            <img src={require('../materials/s1.png')} className='slike_footer'/>*/}
        </div>
        <div className='footer_text'>
            <h3 id='footer_txt'>Milivili</h3>
        </div>
        <div className='pom_el'>
        </div>            
    </div>
  );
  
}

export default FooterC