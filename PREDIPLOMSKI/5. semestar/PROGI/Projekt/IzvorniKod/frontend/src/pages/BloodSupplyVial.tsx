import React from 'react';
import '../styles/BloodVials.css';
interface BloodSupplyVialProps {
  bloodType: string;
  percentageFilled: number;
}

const BloodSupplyVial: React.FC<BloodSupplyVialProps> = ({ bloodType, percentageFilled }) => {
  const validPercentageFilled = Math.min(percentageFilled, 100);

  return (
    <div className="blood-supply-vial">
      <div className="vial-container">
        <div className="vial-filling" style={{ height: `${validPercentageFilled}%` }}></div>
      </div>
      <p className='bsvp'>{bloodType}</p>
    </div>
  );
};

export default BloodSupplyVial;
