import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

import BloodSupplyVial from './BloodSupplyVial';
import '../styles/BloodSuppliesPage.css';

interface BloodSupply {
  id: number;
  amount: number;
  bloodType: string;
  organizationNaziv: string;
}

interface Organization {
  id: string;
  naziv: string;
}

const BloodSuppliesPage: React.FC = () => {
  const [organization, setOrganization] = useState<Organization | null>(null);
  const [bloodSupplies, setBloodSupplies] = useState<BloodSupply[]>([]);
  const [showMessage, setShowMessage] = useState<boolean>(false);
  const [requiredBloodTypes, setRequiredBloodTypes] = useState<string[]>([]);
  const { organizationId } = useParams<{ organizationId: string }>();

  useEffect(() => {
    axios.get(`/api/organization/${organizationId}`)
      .then(response => {
        console.log('Received organization response:', response.data);
        setOrganization(response.data);
      })
      .catch(error => {
        console.error('Error fetching organization:', error);
      });

    axios.get(`/api/organization/${organizationId}/bloodSupplies`)
      .then(response => {
        console.log('Received blood supplies response:', response.data);
        setBloodSupplies(response.data);

        const belowThresholdSupplies = response.data.filter((supply: BloodSupply) => supply.amount < 200);

        if (belowThresholdSupplies.length > 0) {
          setShowMessage(true);
          setRequiredBloodTypes(belowThresholdSupplies.map((supply: BloodSupply) => supply.bloodType));
        }
      })
      .catch(error => {
        console.error('Error fetching blood supplies:', error);
      });
  }, [organizationId]);

  return (
    <div className="blood-supplies-container">
      <h1>Blood supply for {organization?.naziv || 'N/A'}</h1>

      {showMessage && (
        <div className="message-container">
          <p>Blood supply is below 200 units for the following blood types: {requiredBloodTypes.join(', ')}.</p>
        </div>
      )}

      <table className="blood-supplies-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Quantity (ml)</th>
            <th>Organization Naziv</th>
            <th>Blood Type</th>
          </tr>
        </thead>
        <tbody>
          {bloodSupplies.map(bloodSupply => (
            <tr key={bloodSupply.id}>
              <td>{bloodSupply.id}</td>
              <td>{bloodSupply.amount}</td>
              <td>{bloodSupply.organizationNaziv || 'N/A'}</td>
              <td>{bloodSupply.bloodType || 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="blood-vials-container">
        <h2>Percentage of blood supply stock:</h2>
        {bloodSupplies.map((vial) => (
          <BloodSupplyVial
            key={vial.id}
            bloodType={vial.bloodType}
            percentageFilled={(vial.amount / 1500) * 100}
          />
        ))}
      </div>
    </div>
  );
};

export default BloodSuppliesPage;