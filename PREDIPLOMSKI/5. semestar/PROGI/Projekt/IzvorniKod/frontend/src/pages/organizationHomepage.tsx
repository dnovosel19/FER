import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
import '../styles/OrganizationHomepage.css';

interface DonorDetails {
  id: number;
  username: string;
  bloodType?: string;
  name?: string;
  surname?: string;
  oib?: string;
}

interface DonationDetails {
  id: number;
  time: string;
  bloodType: string;
  organizationName: string;
}
interface LocationDTO {
  id: number;
  name: string;
  coordinates: string;
}
interface OrganizationDetails {
  naziv: string;
}
interface AppointmentDTO {
  id: number;
  startTime: string;
  endTime: string;
  donationActionId: number;
  location: LocationDTO;
}
interface OrganizationHomepageProps {
}


const OrganizationHomepage: React.FC<OrganizationHomepageProps> = (props) => {
  const [organizationDetails, setOrganizationDetails] = useState<OrganizationDetails | null>(null);
  const [appliedDonors, setAppliedDonors] = useState<DonorDetails[]>([]);
  const [donationDetails, setDonationDetails] = useState<DonationDetails[]>([]);
  const [appliedOrganizations, setAppliedOrganizations] = useState<number[]>([]);
  const [selectedDonor, setSelectedDonor] = useState<string | null>(null);
  const { organizationId } = useParams<{ organizationId: string }>();
  const [appointments, setAppointments] = useState<AppointmentDTO[]>([]);
  const [selectedDonorDetails, setSelectedDonorDetails] = useState<DonorDetails | null>(null);


  useEffect(() => {
    if (organizationId) {
      axios.get(`/api/organization/${organizationId}`).then((response) => {
        setOrganizationDetails(response.data);
      });

      axios.get(`/api/donation/appliedDonors/${organizationId}`).then((response: any) => {
        if (Array.isArray(response.data) && typeof response.data[0] === 'string') {
          const donorDetailsArray: DonorDetails[] = response.data.map((username: any) => ({
            id: null,
            username,
          }));
          setAppliedDonors(donorDetailsArray);
        } else {
          const donorDetailsArray: DonorDetails[] = response.data.map((donor: any) => ({
            id: donor.id,
            username: donor.username,
            bloodType: donor.bloodType,
            name: donor.name,
            surname: donor.surname,
            oib: donor.oib,
          }));
          setAppliedDonors(donorDetailsArray);
        }
      });
      axios.get(`/api/donation/appliedDonations/${organizationId}`).then((response) => {
        const donationDetailsArray: DonationDetails[] = response.data.map((donation: any) => ({
          id: donation.id,
          time: donation.time,
          bloodType: donation.bloodType,
          organizationName: donation.organizationName,
        }));
        setDonationDetails(donationDetailsArray);
      });

      const storedAppliedOrgs = localStorage.getItem('appliedOrganizations');
      if (storedAppliedOrgs) {
        const appliedOrgIds = JSON.parse(storedAppliedOrgs);
        setAppliedOrganizations(appliedOrgIds);
      }
    }
  }, [organizationId]);

  useEffect(() => {
    const fetchAppointmentsForOrganization = async () => {
      try {
        const response = await axios.get(`/api/organization/${organizationId}/appointments`);
        setAppointments(response.data as AppointmentDTO[]);
      } catch (error) {
        console.error('Error fetching appointments for organization:', error);
        alert('Error fetching appointments. Please try again.');
      }
    };
    fetchAppointmentsForOrganization();
  }, [organizationId]);

  const handleAccept = (donorUsername: string) => {
    const selectedDonorDetail = appliedDonors.find((donor) => donor.username === donorUsername);

    if (selectedDonorDetail) {
      setSelectedDonorDetails(selectedDonorDetail);
      setSelectedDonor(donorUsername);
    }
  };



  const confirmAccept = () => {
    console.log(appointments.length);
    if (selectedDonorDetails && appointments.length > 0) {
      const { id: donorId } = selectedDonorDetails;
      const { id: appointmentId } = appointments[0];

      console.log('Donor ID:', donorId);
      console.log('Appointment ID:', appointmentId);

      axios
        .post('/api/donation/acceptApplication', {
          organizationId,
          donorUsername: selectedDonor,
          donorId,
          appointmentId,
          donationId: donationDetails[0].id,
        })
        .then((response) => {
          console.log(response.data);
          setAppliedDonors((prevDonors) => prevDonors.filter((donor) => donor.username !== selectedDonor));
        })
        .catch((error) => {
          console.error('Error accepting donation application:', error);
        })
        .finally(() => {
          setSelectedDonor(null);
          setSelectedDonorDetails(null);
        });
    }
  };


  const handleReject = (donorUsername: string) => {
    setSelectedDonor(donorUsername);
  };

  const confirmReject = () => {
    if (selectedDonor) {
      axios
        .post(`/api/donation/rejectApplication`, {
          organizationId,
          donorUsername: selectedDonor,
          donationId: donationDetails[0].id,
        })
        .then((response) => {
          setAppliedOrganizations((prevAppliedOrganizations) => {
            const index = prevAppliedOrganizations.indexOf(Number(organizationId));
            if (index !== -1) {
              const updatedAppliedOrganizations = [...prevAppliedOrganizations];
              updatedAppliedOrganizations.splice(index, 1);

              localStorage.setItem('appliedOrganizations', JSON.stringify(updatedAppliedOrganizations));

              return updatedAppliedOrganizations;
            } else {
              console.error('Organization ID not found in the applied organizations array.');
              console.log('organizationId:', organizationId);
              console.log('prevAppliedOrganizations:', prevAppliedOrganizations);
              return prevAppliedOrganizations;
            }
          });

          setAppliedDonors((prevDonors) => prevDonors.filter((donor) => donor.username !== selectedDonor));
        })
        .catch((error) => console.error('Error rejecting application:', error))
        .finally(() => {
          setSelectedDonor(null);
        });
    }
  };
  return (
    <div className="organization-homepage">
      <h1>{organizationDetails?.naziv || 'Organization Name'}</h1>

      <div className="applied-donors-section">
        <h2>Donors who applied for donation:</h2>
        <div className="donors-list giant-donor-list">
          {appliedDonors.length === 0 ? (
            <p>No donors have applied yet.</p>
          ) : (
            <ul>
              {appliedDonors.map((donor, index) => (
                <li key={`${donor.id}_${index}`} className="giant-donor-card">
                  <table>
                    <tbody>
                      <tr>
                        <td><strong>Donor ID:</strong></td>
                        <td>{donor.id}</td>
                      </tr>
                      <tr>
                        <td><strong>Username:</strong></td>
                        <td>{donor.username}</td>
                      </tr>
                      {donor.name && (
                        <tr>
                          <td><strong>Name:</strong></td>
                          <td>{donor.name}</td>
                        </tr>
                      )}
                      {donor.surname && (
                        <tr>
                          <td><strong>Surname:</strong></td>
                          <td>{donor.surname}</td>
                        </tr>
                      )}
                      {donor.oib && (
                        <tr>
                          <td><strong>OIB:</strong></td>
                          <td>{donor.oib}</td>
                        </tr>
                      )}
                    </tbody>
                  </table>

                  {donationDetails.length > index && (
                    <div>
                      <table>
                        <tbody>
                          <tr>
                            <td><strong>Donation ID:</strong></td>
                            <td>{donationDetails[index].id}</td>
                          </tr>
                          <tr>
                            <td><strong>Time:</strong></td>
                            <td>{donationDetails[index].time}</td>
                          </tr>
                          <tr>
                            <td><strong>Blood Type:</strong></td>
                            <td>{donationDetails[index].bloodType}</td>
                          </tr>
                        </tbody>
                      </table>
                      <div className="accept">
                        <button className="accept" onClick={() => handleAccept(donor.username)}>Accept</button>
                      </div>
                      <div className="reject">
                        <button className="reject" onClick={() => handleReject(donor.username)}>Reject</button>
                      </div>
                      {selectedDonor && (
                        <div className="confirmation-modal">
                          <p>Are you sure you want to accept/reject the application for donor: {selectedDonor}?</p>
                          <button className="accept" onClick={confirmAccept}>Accept</button>
                          <button className="reject" onClick={confirmReject}>Reject</button>
                        </div>
                      )}
                    </div>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
      <Link to={`/organization/${organizationId}/bloodSupplies`}>
        Check Blood Supplies Page
      </Link>
    </div>
  );
};

export default OrganizationHomepage;