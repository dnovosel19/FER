import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import '../styles/NagradeSection.css';

interface DonorData {
  donorId: number;
  donationCount: number;
}

interface DonorDetails {
  donorId: number;
  username: string;
  name: string;
  surname: string;
}

interface ExtendedDonorDetails extends DonorDetails, DonorData {}

interface NagradeSectionProps {
  donationsCountData: DonorData[];
}

const NagradeSection: React.FC<NagradeSectionProps> = ({ donationsCountData }) => {
  const [donorDetails, setDonorDetails] = useState<ExtendedDonorDetails[]>([]);
  const [canRemoveReservation, setCanRemoveReservation] = useState<boolean | null>(null);

  useEffect(() => {
    const fetchDonorDetails = async () => {
      const detailsPromises = donationsCountData.map(async (donor) => {
        try {
          const response = await axios.get(`/api/blood_donor/donorInformation/${donor.donorId}`);
          return {
            donorId: donor.donorId,
            username: response.data.username,
            name: response.data.name,
            surname: response.data.surname,
            donationCount: donor.donationCount,
          };
        } catch (error) {
          console.error(`Error fetching donor details for donorId ${donor.donorId}:`, error);
          return null;
        }
      });

      const details = await Promise.all(detailsPromises);
      setDonorDetails(details.filter((detail) => detail !== null) as ExtendedDonorDetails[]);
    };

    fetchDonorDetails();
  }, [donationsCountData]);

  useEffect(() => {
    const checkDonorAppointment = async () => {
      try {
        const response = await axios.get("/api/donation/exists");
        setCanRemoveReservation(!response.data);
      } catch (error) {
        console.error("Error checking donor appointment:", error);
        setCanRemoveReservation(null);
      }
    };

    checkDonorAppointment();
  }, []);

  const sortedDonors = [...donorDetails].sort((a, b) => b.donationCount - a.donationCount);

  return (
    <div id="nagrade">
      <h2>Donations Leaderboard</h2>
      <table className="donors-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Surname</th>
            <th>Donation Count</th>
          </tr>
        </thead>
        <tbody>
          {sortedDonors.map((donor: ExtendedDonorDetails, index) => (
            <tr key={donor.donorId}>
              <td>{index + 1}</td>
              <td>{donor.name}</td>
              <td>{donor.surname}</td>
              <td>{donor.donationCount}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default NagradeSection;