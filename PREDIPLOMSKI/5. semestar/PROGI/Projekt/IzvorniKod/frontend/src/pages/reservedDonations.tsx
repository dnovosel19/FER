import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import '../styles/ReservedDonations.css';
import { Button } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

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
  const { donorId } = useParams<{ donorId?: string }>();
  const [appliedOrganizations, setAppliedOrganizations] = useState<number[]>([]);
  const [isDonorAppointmentExists, setIsDonorAppointmentExists] = useState<boolean>(false);
  const [donorAppointmentId, setDonorAppointmentId] = useState<number | undefined>(undefined);
  const navigate = useNavigate();

  const fetchData = async () => {
    if (!donorId) return;

    try {
      const donorAppointmentExists = await checkDonorAppointmentExists(parseInt(donorId, 10));
      setIsDonorAppointmentExists(donorAppointmentExists);
    } catch (error) {
      console.error('Error checking donor appointment:', error);
    }

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
  };

  useEffect(() => {
    fetchData();
  }, [donorId]);

  const handleRemoveReservation = (donationId: number, organizationId: number) => {
    axios
      .post('/api/donation/removeApplication', {
        donorId: donorId,
        donationId: donationId,
      })
      .then((response) => {
        console.log('Reservation removed successfully:', response.data);

        if (appliedOrganizations.includes(organizationId)) {
          setAppliedOrganizations((prevAppliedOrganizations) =>
            prevAppliedOrganizations.filter((orgId) => orgId !== organizationId)
          );

          const updatedAppliedOrgs = appliedOrganizations.filter((orgId) => orgId !== organizationId);
          localStorage.setItem('appliedOrganizations', JSON.stringify(updatedAppliedOrgs));
        }

        fetchData();
      })
      .catch((error) => {
        console.error('Error removing reservation:', error);
        alert('Error removing reservation. Please try again.');
      });
  };

  const checkDonorAppointmentExists = async (donorId: number): Promise<boolean> => {
    try {
      const response = await axios.get(`/api/donation/exists`);

      if (response.data && response.data.length > 0 && response.data[0].id !== undefined) {
        const appointmentId = response.data[0].id;
        setDonorAppointmentId(appointmentId);
        return true;
      } else {
        console.error('No donations with donor appointments');
        return false;
      }
    } catch (error) {
      console.error('Error checking donor appointment:', error);
      return false;
    }
  };

  const isToday = (reservationDate: string): boolean => {
    const today = new Date();
    const reservationDateTime = new Date(reservationDate);

    return (
      today.getDate() === reservationDateTime.getDate() &&
      today.getMonth() === reservationDateTime.getMonth() &&
      today.getFullYear() === reservationDateTime.getFullYear()
    );
  };

  return (
    <div className='velika-stranica'>
      <div className="reserved-donations-container">
        <h1>My reserved donations:</h1>
        <Button className="btnpip" variant="outlined" startIcon={<ArrowBackIcon/>} sx={{position:'absolute', top: 100, left: 100, color: 'white', bgcolor: 'red', '&:hover': { bgcolor: '', borderColor: 'red', color: 'black', '& svg': {visibility: 'visible'} } }} onClick={() => navigate(-1)}>Go back</Button>
        <table className="reserved-donations-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Blood Type</th>
              <th>Location</th>
              <th>Organization</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {reservedDonations
              .filter((reservedDonation) => isToday(reservedDonation.time))
              .map((reservedDonation) => (
              <tr key={reservedDonation.id}>
                <td>{reservedDonation.time}</td>
                <td>{reservedDonation.bloodType}</td>
                <td>{reservedDonation.location.name}</td>
                <td>{reservedDonation.organization.naziv}</td>
                <td>
                    <button
                      onClick={() => handleRemoveReservation(reservedDonation.id, reservedDonation.organization.id)}
                    >
                      Remove Reservation
                    </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
export default ReservedDonationsPage;