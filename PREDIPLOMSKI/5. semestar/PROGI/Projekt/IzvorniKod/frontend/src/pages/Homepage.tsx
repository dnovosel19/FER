import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import BloodSupplyVial from './BloodSupplyVial';
import '../styles/Homepage.css';
import NagradeSection from './NagradeSection';
import DarivanjeKrviSection from './DarivanjeKrviSection';
import CestaPitanjaSection from './CestaPitanjaSection';
import { AppBar, Box, Button, IconButton, ListItemIcon, Menu, MenuItem, TextField, Toolbar } from '@mui/material';
import MapIcon from '@mui/icons-material/Map';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import LogoutIcon from '@mui/icons-material/Logout';
import MenuIcon from '@mui/icons-material/Menu';
import { cursorTo } from 'readline';
import { ClassNames } from '@emotion/react';
import MapComponent from '../components/Marker';

interface OrganizationDTO {
  id: number;
  adminUsername: string;
  adminPassword: string;
  adminName: string;
  adminSurname: string;
  locationId: number;
  organizationTypeId: number;
  naziv: string;
}

interface BloodSupplyVial {
  id: number;
  amount: number;
  bloodType: string;
  organizationNaziv: string;
}

interface LocationDTO {
  id: number;
  name: string;
  coordinates: string;
}

interface AppointmentDTO {
  id: number;
  startTime: string;
  endTime: string;
  donationActionId: number;
  location: LocationDTO;
}

interface BloodSupply {
  id: number;
  amount: number;
  bloodType: string;
  organizationNaziv: string;
}

const options = ['Profile', 'My reserved donations', 'Donation history'];
const ITEM_HEIGHT = 48;

const Homepage: React.FC = () => {
  const { donorId } = useParams();
  const [organizations, setOrganizations] = useState<OrganizationDTO[]>([]);
  const [selectedOrganization, setSelectedOrganization] = useState<OrganizationDTO | null>(null);
  const [donorUsername, setDonorUsername] = useState<string>('');
  const [selectedBloodGroup, setSelectedBloodGroup] = useState<string>('');
  const [hasApplied, setHasApplied] = useState<boolean>(false);
  const [isApplicationSubmitted, setIsApplicationSubmitted] = useState<boolean>(false);
  const [appliedOrganizations, setAppliedOrganizations] = useState<number[]>(() => {
    const storedAppliedOrgs = sessionStorage.getItem('appliedOrganizations');
    return storedAppliedOrgs ? JSON.parse(storedAppliedOrgs) : [];
  });
  const [appointments, setAppointments] = useState<AppointmentDTO[]>([]);
  const [organizationBloodSupplies, setOrganizationBloodSupplies] = useState<BloodSupply[]>([]);
  const [showBloodSupplies, setShowBloodSupplies] = useState(false);
  const [bloodSupplyMessage, setBloodSupplyMessage] = useState<string>('');
  const [searchLocation, setSearchLocation] = useState<string>('');
  const [searchOrganization, setSearchOrganization] = useState<string>('');
  const [bloodVials, setBloodVials] = useState<BloodSupplyVial[]>([]);
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState<boolean>(false);
  const [newName, setNewName] = useState<string>('');
  const [newSurname, setNewSurname] = useState<string>('');
  const [newUsername, setNewUsername] = useState<string>('');
  const [newPassword, setNewPassword] = useState<string>('');
  const [isApplying, setIsApplying] = useState<boolean>(false);
  const [donationsCountData, setDonationsCountData] = useState<any[]>([]);

  const [isOrganizationSelected, setIsOrganziationSelected] = useState<boolean>(false);
  const [isMapVisible, setIsMapVisible] = useState<boolean>(false);
  const [showMap, setShowMap] = useState<boolean>(false);
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
    setShowMap(false);
  };

  const handleToggleMap = () => {
    // setShowMap((prevShowMap) => !prevShowMap);
    if (!isOrganizationSelected) {
      setIsMapVisible((prevIsMapVisible) => !prevIsMapVisible);
    }
  };

  const handleMenuClick = (option: string) => {
    switch (option) {
      case 'Profile':
        navigate(`/changeSettings/${donorId}`);
        break;
      case 'My reserved donations':
        navigate(`/reservedDonations/${donorId}`);
        break;
      case 'Donation history':
        navigate(`/donationHistory/${donorId}`);
        break;
      default:
        break;
    }

    handleClose();
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/donation/donationCount');
        const data = await response.json();
        console.log(data);
        setDonationsCountData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);
  useEffect(() => {
    if (organizationBloodSupplies.some((supply) => supply.amount < 200)) {
      setShowBloodSupplies(false);
      checkBloodSupplies(selectedOrganization?.id || 0);
    }
  }, [organizationBloodSupplies, selectedOrganization]);
  const handleDropdownClick = () => {
    setShowDropdown(!showDropdown);
  };

//   const handleDropdownOptionClick = async (action: string) => {
//     switch (action) {
//       case 'changeSettings':
//         navigate(`/changeSettings/${donorId}`);
//         break;
//       case 'reservedDonations':
//         navigate(`/reservedDonations/${donorId}`);
//         break;
//       case 'donationHistory':
//         navigate(`/donationHistory/${donorId}`);
//         break;
//       default:
//         break;
//     }
//
//     setShowDropdown(false);
//   };

//   const updateName = async (newName: string) => {
//     try {
//       await axios.put(`/api/blood_donor/changeName/${donorId}`, {
//         newName,
//       });
//
//       alert('Name changed successfully.');
//     } catch (error) {
//       console.error('Error changing name:', error);
//       alert('Error changing name. Please try again.');
//     }
//   };

  const handleDismissMessage = () => {
    setBloodSupplyMessage('');
  };

  useEffect(() => {
    const fetchBloodVials = async () => {
      try {
        if (selectedOrganization && selectedOrganization.id) {
          const response = await axios.get(`/api/organization/${selectedOrganization.id}/bloodSupplies`);
          setBloodVials(response.data as BloodSupplyVial[]);
        }
      } catch (error) {
        console.error('Error fetching blood vials:', error);
        alert('Error fetching blood vials. Please try again.');
      }
    };

    fetchBloodVials();
  }, [selectedOrganization]);

  const renderBloodVials = () => {
    return (
      <div className="blood-vials-container">
        {bloodVials.map((vial) => (
          <div key={vial.id} className="blood-vial">
            <div className="blood-vial-label">{vial.bloodType}</div>
            <div className="blood-vial-amount" style={{ height: `${(vial.amount / 1500) * 100}%` }}></div>
          </div>
        ))}
      </div>
    );
  };
  const handleSearch = () => {
    const fetchOrganizations = async () => {
      try {
        let url = '/api/organization/allOrganizations';

        if (searchLocation) {
          url += `?location=${searchLocation}`;
        }

        const organizationsResponse = await axios.get(url);
        setOrganizations(organizationsResponse.data as OrganizationDTO[]);
      } catch (error) {
        console.error('Error fetching organizations:', error);
        alert('Error fetching organizations. Please try again.');
      }
    };

    fetchOrganizations();
  };

  const handleOrganizationSelect = (selectedOrgId: number) => {
    const selectedOrg = organizations.find((org) => org.id === selectedOrgId);
    setSelectedOrganization(selectedOrg || null);
    setShowBloodSupplies(false);
    setIsMapVisible(false);
    setIsOrganziationSelected(true);

    if (selectedOrg && selectedOrg.id) {
      checkBloodSupplies(selectedOrg.id);
    }
  };

  const checkBloodSupplies = async (orgId: number) => {
    try {
      const response = await axios.get(`/api/organization/${orgId}/bloodSupplies`);
      const organizationBloodSupplies = response.data as BloodSupply[];

      const lowBloodSupplies = organizationBloodSupplies.filter((supply) => supply.amount < 200);

      if (lowBloodSupplies.length > 0) {
        const bloodSupplyMessage = `Zalihe krvi za ${selectedOrganization?.naziv} su ispod 200 ml za sljedeće krvne grupe: ${lowBloodSupplies
          .map((supply) => supply.bloodType)
          .join(', ')}. Razmislite o donaciji.`;

        setBloodSupplyMessage(bloodSupplyMessage);
      } else {
        setBloodSupplyMessage('');
      }
    } catch (error) {
      console.error('Error checking blood supplies for organization:', error);
      alert('Error checking blood supplies. Please try again.');
    }
  };

  useEffect(() => {
    console.log('Appointments Length:', appointments.length);
  }, [appointments]);

  useEffect(() => {
    const fetchAppointmentsForOrganization = async () => {
      if (selectedOrganization && selectedOrganization.id) {
        try {
          const response = await axios.get(`/api/organization/${selectedOrganization.id}/appointments`);
          console.log('Appointments Response:', response.data);

          console.log('Selected Organization ID:', selectedOrganization.id);

          setAppointments(response.data as AppointmentDTO[]);
        } catch (error) {
          console.error('Error fetching appointments for organization:', error);
          alert('Error fetching appointments. Please try again.');
        }
      }
    };

    const fetchBloodSuppliesForOrganization = async () => {
      if (selectedOrganization && selectedOrganization.id) {
        try {
          const response = await axios.get(`/api/organization/${selectedOrganization.id}/bloodSupplies`);
          setOrganizationBloodSupplies(response.data as BloodSupply[]);
        } catch (error) {
          console.error('Error fetching blood supplies for organization:', error);
          alert('Error fetching blood supplies. Please try again.');
        }
      }
    };

    fetchAppointmentsForOrganization();
    fetchBloodSuppliesForOrganization();
  }, [selectedOrganization]);

  useEffect(() => {
    const storedAppliedOrgs = localStorage.getItem('appliedOrganizations');

    if (storedAppliedOrgs) {
      const appliedOrgIds = JSON.parse(storedAppliedOrgs);
      setAppliedOrganizations(appliedOrgIds);
    }
  }, []);
  const fetchData = async () => {
    try {
      const donorInformationResponse = await axios.get(`/api/blood_donor/donorInformation/${donorId}`);
      const organizationsResponse = await axios.get('/api/organization/allOrganizations');

      const donorInformation = donorInformationResponse.data;
      const organizations = organizationsResponse.data as OrganizationDTO[];
      setOrganizations(organizations);
      setDonorUsername(donorInformation.username);

      localStorage.setItem('donorUsername', donorInformation.username);
    } catch (error) {
      console.error('Error fetching data:', error);
      alert('Error fetching data. Please try again.');
    }
  };

  useEffect(() => {
    const fetchDataAndAppointments = async () => {
      try {
        await fetchData();
        if (selectedOrganization && selectedOrganization.id) {
          console.log('Fetching appointments for organization:', selectedOrganization.id);
          const appointmentsResponse = await axios.get(`/api/organization/${selectedOrganization.id}/appointments`);
          console.log('Appointments Response:', appointmentsResponse.data);
          setAppointments(appointmentsResponse.data as AppointmentDTO[]);
        }
      } catch (error) {
        console.error('Error fetching data or appointments:', error);
        alert('Error fetching data or appointments. Please try again.');
      }
    };

    fetchDataAndAppointments();
  }, [donorId, selectedOrganization]);


  const handleReject = (organizationId: number) => {
    axios
      .post(`/api/donation/rejectApplication`, {
        organizationId,
        donorUsername,
      })
      .then((response) => {
        setAppliedOrganizations((prevAppliedOrganizations) =>
          prevAppliedOrganizations.filter((orgId) => orgId !== organizationId)
        );
      })
      .catch((error) => console.error('Error rejecting application:', error));
  };

  const handleApplyDonation = () => {
    if (selectedOrganization && selectedOrganization.id) {

      const isConfirmed = window.confirm('Are you sure you want to apply for donation?');

      if (isConfirmed) {
        setIsApplying(true);

        axios
          .post(`/api/donation/apply`, {
            organizationId: selectedOrganization.id,
            donorUsername: donorUsername,
            selectedBloodGroup: selectedBloodGroup,
          })
          .then((response) => {
            console.log('Donation application successful:', response.data);

            setAppliedOrganizations((prevAppliedOrganizations) => [
              ...prevAppliedOrganizations,
              selectedOrganization.id,
            ]);

            const donorId = response.data?.bloodDonorId;

            if (donorId !== undefined) {
              navigate(`/homepage/${donorId}`);
            } else {
              console.error('Error: Missing donor ID in the response.');
              alert('Error applying for donation. Please try again.');
            }

            fetchData();
          })
          .catch((error) => {
            console.error('Error applying for donation:', error);
            alert('Error applying for donation. Please try again.');
          })
          .finally(() => {
            setIsApplying(false);
          });
      }
    } else {
      console.log('Invalid data. No organization selected.');
    }
  };

  useEffect(() => {
    sessionStorage.setItem('appliedOrganizations', JSON.stringify(appliedOrganizations));
  }, [appliedOrganizations]);


  const handleOrganizationClick = (organization: OrganizationDTO) => {
    setSelectedOrganization((prevSelected) => (prevSelected === organization ? null : organization));
    setShowBloodSupplies(false);
  };

  const handleShowBloodSupplies = () => {
    setShowBloodSupplies(!showBloodSupplies);
  };
  const scrollToSection = (sectionId: string) => {
    const sectionElement = document.getElementById(sectionId);
    if (sectionElement) {
      sectionElement.scrollIntoView({ behavior: 'smooth' });
    }
  };
  const handleLogoutClick = () => {
    try{
    axios.get("/api/logout").then(function (response){
        localStorage.clear();
        navigate('/');
        window.location.reload();
    });
    }
    catch (error){
      console.error('Error logging out:', error);
      alert('Error logging out. Please try again.');
    }
  };

  return (
    <Box className="boxx" sx={{flexGrow: 1}}>
      <AppBar position='static'>
        <Toolbar sx={{justifyContent: 'space-between', backgroundColor: 'red'}}>
          <IconButton size='large' edge='start' color='inherit' aria-label='menu' id='long-button' aria-controls={open ? 'long-menu' : undefined} aria-expanded={open ? 'true' : undefined} aria-haspopup='true' onClick={handleClick}>
            <MenuIcon/>
          </IconButton>

          {/* <div className='curs-poi' onClick={() => scrollToSection('kontakt')}>Contact</div> */}
          <div className='curs-poi' onClick={() => scrollToSection('nagrade')}>Awards</div>
          <div className='curs-poi' onClick={() => scrollToSection('darivanjeKrvi')}>Blood donation</div>
          <div className='curs-poi' onClick={() => scrollToSection('cestaPitanja')}>FAQ</div>
          <div className='curs-ptr'>{donorUsername && <span>{donorUsername}</span>}</div>

          <Menu id='long-menu' MenuListProps={{'aria-labelledby' : 'long-button'}} anchorEl={anchorEl} open={open} onClose={handleClose} PaperProps={{style: {maxHeight: ITEM_HEIGHT*4.5, width: '25ch'}}}>
            {options.map((option) => (
              <MenuItem key={option} selected={option === 'Pyxis'} onClick={() => handleMenuClick(option)}>
                {option === 'Profile' && (
                  <ListItemIcon>
                    <AccountCircleIcon/>
                  </ListItemIcon>
                )}
                {option}
              </MenuItem>
            ))}
          </Menu>
          <IconButton size='large' edge='end' color='inherit' title='Logout' onClick={handleLogoutClick}>
            <LogoutIcon/>
          </IconButton>
        </Toolbar>
      </AppBar>
      <div className="homepage-container">
        {/* <div className="dropdown-container">
          <div className="footer">
            <button className="dropdown-button" onClick={handleDropdownClick}>
              ☰
            </button>
            <div onClick={() => scrollToSection('kontakt')}>Kontakt</div>
            <div onClick={() => scrollToSection('nagrade')}>Nagrade</div>
            <div onClick={() => scrollToSection('darivanjeKrvi')}>Darivanje krvi</div>
            <div onClick={() => scrollToSection('cestaPitanja')}>Česta pitanja</div>
            <div onClick={() => scrollToSection('kontakt')}>Kontakt</div>
            <div>
              {donorUsername && <span className="logout">{donorUsername}</span>}
              <button onClick={handleLogoutClick}>Logout</button>
            </div>
          </div>
          {showDropdown && (
            <div className="dropdown-options">
              <div className="dropdown-option" onClick={() => handleDropdownOptionClick('changeSettings')}>
                Change personal information
              </div>
              <div className="dropdown-option" onClick={() => handleDropdownOptionClick('reservedDonations')}>
                My reserved donations
              </div>
              <div className="dropdown-option" onClick={() => handleDropdownOptionClick('donationHistory')}>
                Donation History
              </div>
            </div>
          )}
        </div> */}

        <h1>Welcome back {donorUsername}!</h1>
        
        <Box sx={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2, ml: 4}}>
          <Button variant='outlined' onClick={handleToggleMap} disabled={isOrganizationSelected} sx={{borderRadius: '15px', overflow: 'hidden', color: isOrganizationSelected ? 'black' : 'white', bgcolor: isOrganizationSelected ? 'grey' :'red', '&:hover': { bgcolor: isOrganizationSelected ? 'grey' : '', borderColor: 'blue', color: 'black', '& svg': {visibility: 'visible'} } }}>
            {isMapVisible ? (
              <>
                <MapIcon/>&nbsp;Hide map
              </>
            ) : (
              <>
                <MapIcon/>&nbsp;Show map
              </>
            )}
          </Button>
          <TextField className='organization' select label='Choose organization' onChange={(e) => handleOrganizationSelect(Number(e.target.value))} variant='standard' required={false} style={{marginRight: '20px'}}>
            {organizations.map((organization: OrganizationDTO) => (
              <MenuItem key={organization.id} value={organization.id}>
                {organization.naziv}
              </MenuItem>
            ))}
          </TextField>
        </Box>

        {isMapVisible && <MapComponent/>}

        {/* <div className="organization-dropdown-container">
          <label htmlFor="organizationDropdown">Odaberi organizaciju:</label>
          <select
            id="organizationDropdown"
            onChange={(e) => handleOrganizationSelect(Number(e.target.value))}
          >
            <option value="">-- Odaberi organizaciju --</option>
            {organizations.map((organization: OrganizationDTO) => (
              <option key={organization.id} value={organization.id}>
                {organization.naziv}
              </option>
            ))}
          </select>
        </div> */}

        {selectedOrganization && (
          <div className="selected-info">
            <h2>{selectedOrganization.naziv}</h2>
            {bloodSupplyMessage && (
              <div className="blood-supply-message">
                <p>
                  Blood supplies for {selectedOrganization?.naziv} are below 200ml for the following blood groups:
                </p>
                <ul>
                  {organizationBloodSupplies
                    .filter((supply) => supply.amount < 200)
                    .map((supply) => (
                      <li key={supply.id}>
                        Blood group: {supply.bloodType}
                      </li>
                    ))}
                </ul>
                <p>Please consider donating.</p>
                <button className='hombtn' onClick={handleDismissMessage}>Dismiss</button>
              </div>
            )}
            {hasApplied ? (
              <p>You have already applied for this organization.</p>
            ) : (
              <>
                {appointments.length > 0 && (
                  <div>
                    <ul>
                      {appointments.map((appointment) => (
                        <li key={appointment.id}>
                          {`From: ${appointment.startTime}, To: ${appointment.endTime}, Location: ${appointment.location.name}`}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {/* <label htmlFor="bloodGroup">Choose the blood type you donate:</label>
                <select
                  id="bloodGroup"
                  value={selectedBloodGroup}
                  onChange={(e) => setSelectedBloodGroup(e.target.value)}
                >
                  <option value="">-- Krvna grupa --</option>
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="0-">0--</option>
                  <option value="0+">0+</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                </select> */}

                <TextField className="blood-group" id="bloodGroup" select label="Choose the blood type you donate:" value={selectedBloodGroup} onChange={(e) => setSelectedBloodGroup(e.target.value)} variant="standard" required={false}>
                    {["0+", "0-", "AB+", "AB-", "A+", "A-", "B+", "B-"].map((value: string) => (
                        <MenuItem key={value} value={value}>{value}</MenuItem>
                    ))}
                </TextField>

                <button
                  onClick={handleApplyDonation}
                  disabled={!selectedBloodGroup || isApplying}
                  className={isApplying ? 'applying' : ''}
                >
                  {isApplying ? 'Applying...' : 'Apply me for donation'}
                </button>
                <button className='hombtn' onClick={handleShowBloodSupplies}>
                  {showBloodSupplies ? 'Hide blood supplies' : 'Show blood supplies'}
                </button>
              </>
            )}
          </div>
        )}

        {showBloodSupplies && organizationBloodSupplies.length > 0 && (
          <div className="blood-supplies-section">
            <h2 className='nasl1'>Blood supplies for {selectedOrganization?.naziv || 'N/A'}</h2>
            <table className='tbl'>
              <thead>
                <tr>
                  <th className='abc'>ID</th>
                  <th className='abc'>Quantity (ml)</th>
                  <th className='abc'>Organization name</th>
                  <th className='abc'>Blood Type</th>
                </tr>
              </thead>
              <tbody>
                {organizationBloodSupplies.map((bloodSupply) => (
                  <tr key={bloodSupply.id}>
                    <td className='cba'>{bloodSupply.id}</td>
                    <td className='cba'>{bloodSupply.amount}</td>
                    <td className='cba'>{bloodSupply.organizationNaziv || 'N/A'}</td>
                    <td className='cba'>{bloodSupply.bloodType || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>

          </div>
        )}
        {showBloodSupplies && (
          <div className="blood-supplies-section">
            <h2>Percentage of blood supplies filled</h2>
            <div className="vials-container">
              {bloodVials.map((vial) => (
                <BloodSupplyVial
                  key={vial.id}
                  bloodType={vial.bloodType}
                  percentageFilled={(vial.amount / 1500) * 100}
                />
              ))}
            </div>
          </div>
        )}
        <DarivanjeKrviSection />
        <CestaPitanjaSection />
        {donationsCountData.length > 0 && (
          <NagradeSection donationsCountData={donationsCountData} />
        )}
      </div>
    </Box>
  );
};
export default Homepage;