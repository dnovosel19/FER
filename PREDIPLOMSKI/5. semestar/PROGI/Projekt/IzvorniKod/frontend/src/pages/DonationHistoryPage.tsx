import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import '../styles/ReservedDonations.css';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { Button } from '@mui/material';

interface LocationDTO {
  id: number;
  name: string;
  coordinates: string;
}

interface OrganizationDTO {
  id: number;
  naziv: string;
}

interface ReservedDonation {
  id: number;
  time: string;
  bloodType: string;
  location: LocationDTO;
  organization: OrganizationDTO;
}

const ReservedDonationsPage: React.FC = () => {
  const [reservedDonations, setReservedDonations] = useState<ReservedDonation[]>([]);
  const { donorId } = useParams<{ donorId: string }>();
  const [appliedOrganizations, setAppliedOrganizations] = useState<number[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`/api/donation/reservedDonations/${donorId}`)
      .then(response => {
        console.log('Received reserved donations response:', response.data);
        setReservedDonations(response.data);
      })
      .catch(error => {
        console.error('Error fetching reserved donations:', error);
      });

    const storedAppliedOrgs = localStorage.getItem('appliedOrganizations');
    if (storedAppliedOrgs) {
      const appliedOrgIds = JSON.parse(storedAppliedOrgs);
      setAppliedOrganizations(appliedOrgIds);
    }
  }, [donorId]);

  return (
    <div className='velika-stranica'>
      <div className="reserved-donations-container">
        <h1>History of blood donation:</h1>
        <Button className="btnpip" variant="outlined" startIcon={<ArrowBackIcon/>} sx={{position:'absolute', top: 100, left: 100, color: 'white', bgcolor: 'red', '&:hover': { bgcolor: '', borderColor: 'red', color: 'black', '& svg': {visibility: 'visible'} } }} onClick={() => navigate(-1)}>Go back</Button>
        <table className="reserved-donations-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Blood Type</th>
              <th>Location</th>
              <th>Organization</th>
            </tr>
          </thead>
          <tbody>
            {reservedDonations.map(reservedDonation => (
              <tr key={reservedDonation.id}>
                <td>{reservedDonation.time}</td>
                <td>{reservedDonation.bloodType}</td>
                <td>{reservedDonation.location.name}</td>
                <td>{reservedDonation.organization.naziv}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ReservedDonationsPage;