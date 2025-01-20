import React, { useState } from 'react';
import '../styles/DarivanjeKrvi.css';

interface InfoData {
  zasto: string;
  tko: string;
  gdje: string;
  kako: string;
  preporuka: string;
}

const DarivanjeKrvi: React.FC = () => {
  const [selectedInfo, setSelectedInfo] = useState<string | null>(null);
  const [selectedKey, setSelectedKey] = useState<keyof InfoData | null>(null);

  const infoData: InfoData = {
    zasto:
      'Blood cannot be manufactured; the only source of this medicine is a human – a blood donor. Every day, numerous patients require treatment with blood products. Therefore, to ensure an adequate supply of blood products, it is essential to always have a sufficient number of donors. You can donate whole blood and/or blood components using a cell separator. Blood components can only be donated at the Croatian Institute of Transfusion Medicine after donating whole blood several times.',
      tko: 'Any person in good general health, aged between 18 and 65 years (up to 60 years for first-time donors), weighing over 55 kilograms, and with a body temperature below 37°C can donate blood.',
    gdje: 'You can donate blood at the Croatian Institute for Transfusion Medicine (CITM) every working day from 07:30 to 19:00 and on Saturdays from 7:30 to 15:00, as well as at organized blood donation events organized by City Red Cross Societies (locations and times of events available on our website).',
    kako: 'You can check the status of blood supplies for your blood type on our website. If the current blood supplies for your blood type are below the \'insufficient supplies\' mark, please consider donating blood. If the current quantities of blood for your blood type are above the \'excessive supplies\' mark, kindly postpone donation until the supplies for your blood type decrease. Men can donate blood every 3 months (up to 7 days earlier), and women every 4 months (up to 7 days earlier).',
    preporuka: 'Eat a light meal and drink enough non-alcoholic fluids. Bring your ID card or passport and health insurance card. Also, bring the Blood Donor Card so that we can record your donation.',
  };

  const handleInfoClick = (infoKey: keyof InfoData) => {
    if (selectedKey === infoKey) {
      setSelectedKey(null);
      setSelectedInfo(null);
    } else {
      setSelectedKey(infoKey);
      setSelectedInfo(infoData[infoKey]);
    }
  };


  return (
    <div id="darivanjeKrvi" className={`darivanje-container ${selectedKey ? 'clicked' : ''}`}>
          <p className="darivanjeK"><b>Blood Donation</b></p>
      <div className={`info-item ${selectedKey === 'zasto' ? 'active' : ''}`} onClick={() => handleInfoClick('zasto')}>
        {selectedKey === 'zasto' ? '▲' : '▼'} Why should I donate blood?
      </div>
      {selectedKey === 'zasto' && (
        <div className="info-dropdown">
          <p>{selectedInfo}</p>
        </div>
      )}
      <div className={`info-item ${selectedKey === 'tko' ? 'active' : ''}`} onClick={() => handleInfoClick('tko')}>
        {selectedKey === 'tko' ? '▲' : '▼'} Who can donate blood?
      </div>
      {selectedKey === 'tko' && (
        <div className="info-dropdown">
          <p>{selectedInfo}</p>
        </div>
      )}
      <div className={`info-item ${selectedKey === 'gdje' ? 'active' : ''}`} onClick={() => handleInfoClick('gdje')}>
        {selectedKey === 'gdje' ? '▲' : '▼'} Where can I donate blood?
      </div>
      {selectedKey === 'gdje' && (
        <div className="info-dropdown">
          <p>{selectedInfo}</p>
        </div>
      )}
      <div className={`info-item ${selectedKey === 'kako' ? 'active' : ''}`} onClick={() => handleInfoClick('kako')}>
        {selectedKey === 'kako' ? '▲' : '▼'} How to donate blood?
      </div>
      {selectedKey === 'kako' && (
        <div className="info-dropdown">
          <p>{selectedInfo}</p>
        </div>
      )}
      <div className={`info-item ${selectedKey === 'preporuka' ? 'active' : ''}`} onClick={() => handleInfoClick('preporuka')}>
        {selectedKey === 'preporuka' ? '▲' : '▼'} Recommendations before blood donation
      </div>
      {selectedKey === 'preporuka' && (
        <div className="info-dropdown">
          <p>{selectedInfo}</p>
        </div>
      )}
    </div>
  );
};

export default DarivanjeKrvi;
