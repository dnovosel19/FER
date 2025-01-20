import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import '../styles/PersonalInformation.css';
import { useNavigate } from 'react-router-dom';
import { Button } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

const PersonalInformation: React.FC = () => {
  const { donorId } = useParams();
  const [name, setName] = useState<string>('');
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [surname, setSurname] = useState<string>('');
  const [oldName, setOldName] = useState<string>('');
  const [newName, setNewName] = useState<string>('');
  const [oldUSername, setOldUsername] = useState<string>('');
  const [newUsername, setNewUsername] = useState<string>('');
  const [oldPassword, setOldPassword] = useState<string>('');
  const [newPassword, setNewPassword] = useState<string>('');
  const [oldSurname, setOldSurname] = useState<string>('');
  const [newSurname, setNewSurname] = useState<string>('');
  const [confirmationModal, setConfirmationModal] = useState<boolean>(false);
  const [fieldToUpdate, setFieldToUpdate] = useState<string>('');
  const validateName = (value: string): boolean => value.length >= 3;
  const validateUsername = (value: string): boolean => value.length > 0;
  const validatePassword = (value: string): boolean => value.length >= 6 && value.length <= 20;
  const [usernameError, setUsernameError] = useState<string>('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`/api/blood_donor/donorInformation/${donorId}`);
        const donorData = response.data;

        setName(donorData.name);
        setSurname(donorData.surname);
        setUsername(donorData.username);
        console.log(donorData.name);
      } catch (error) {
        console.error('Error fetching donor data:', error);
        alert('Error fetching donor data. Please try again.');
      }
    };

    fetchData();
  }, [donorId]);

  const openConfirmationModal = (field: string) => {
    setFieldToUpdate(field);
    setConfirmationModal(true);
  };

  const closeConfirmationModal = () => {
    setFieldToUpdate('');
    setConfirmationModal(false);
  };

  const handleUpdateName = async () => {
    if (oldName === '' || oldName !== name || newName === '' || newName === oldName) {
      alert('Please enter your current name correctly and provide a different new name.');
      return;
    }

    openConfirmationModal('name');
  };
  const handleUpdateSurname = async () => {
      if (oldSurname === '' || oldSurname !== surname || newSurname === '' || newSurname === oldSurname) {
        alert('Please enter your current surname correctly and provide a different new surname.');
        return;
      }

      openConfirmationModal('surname');
    };

  const handleUpdateUsername = async () => {
    if (newUsername === '' || oldUSername === '' || oldUSername !== username) {
      setUsernameError('Please enter your current username correctly and provide a new username.');
      return;
    }

    try {
      const response = await axios.put(`/api/blood_donor/changeUsername/${donorId}`, {
        oldUsername: oldUSername,
        newUsername,
      });

      if (response.status === 200) {
        setUsernameError('');
        openConfirmationModal('username');
      } else {
        setUsernameError(response.data);
      }
    } catch (error) {
      console.error('Error updating username:', error);
      setUsernameError('Error updating username. Please try again.');
    }
  };
const handleUpdatePassword = async () => {
    if (oldPassword === '' || newPassword === '' || newPassword.length < 6) {
      if (oldPassword === '') {
        alert('Please enter your old password.');
      } else if (newPassword === '') {
        alert('Please enter a new password.');
      } else {
        alert('Please enter a new password with at least 6 characters.');
      }
      return;
    }

    openConfirmationModal('password');
  };
  const handleDeleteAccount = async () => {
    const confirmDelete = window.confirm('Are you sure you want to delete your account?');
    if (confirmDelete) {
      try {
        await axios.delete(`/api/blood_donor/deleteAccount/${donorId}`);
        alert('Account deleted successfully.');
        navigate(`/login`);
      } catch (error) {
        console.error('Error deleting account:', error);
        alert('Error deleting account. Please try again.');
      }
    }
  };
  const confirmUpdateField = async () => {
    try {
      switch (fieldToUpdate) {
        case 'name':
          if (newName === '' || newName === oldName) {
            setUsernameError('Please enter a new name.');
            return;
          }
          await axios.put(`/api/blood_donor/changeName/${donorId}`, {
            oldName,
            newName,
          });
          setUsernameError('');
          setName(newName);
          setOldName('');
          setNewName('');
          break;

        case 'username':
          await axios.put(`/api/blood_donor/changeUsername/${donorId}`, {
            oldUSername,
            newUsername,
          });
          setUsernameError('');
          openConfirmationModal('username');
          setUsername(newUsername);
          setOldUsername('');
          setNewUsername('');
          break;

        case 'password':
          await axios.put(`/api/blood_donor/changePassword/${donorId}`, {
            oldPassword,
            newPassword,
          });
          setUsernameError('');
          setOldPassword('');
          setNewPassword('');
          break;

        case 'surname':
          if (newSurname === '' || newSurname === oldSurname) {
            setUsernameError('Please enter a new surname.');
            return;
          }
          await axios.put(`/api/blood_donor/changeSurname/${donorId}`, {
            oldSurname,
            newSurname,
          });
          setUsernameError('');
          setSurname(newSurname);
          setOldSurname('');
          setNewSurname('');
          break;
          
        default:
          break;
      }
    } catch (error) {
      console.error(`Error updating ${fieldToUpdate}:`, error);
      setUsernameError(`Error updating ${fieldToUpdate}. Please try again.`);
    } finally {
      setConfirmationModal(false);
    }
  };
  return (
    <div className="personal-information">
      <Button className="btnpip" variant="outlined" startIcon={<ArrowBackIcon/>} sx={{position:'absolute', top: 100, left: 100, color: 'white', bgcolor: 'red', '&:hover': { bgcolor: '', borderColor: 'red', color: 'black', '& svg': {visibility: 'visible'} } }} onClick={() => navigate(-1)}>Go back</Button>
      <div className="personal-information-container">
        <h1 className="personal-information-title">Personal Information</h1>
        <div className="personal-information-data">
          <div>
            <h2>Name: {name}</h2>
            <input
              className='txt1'
              type="text"
              placeholder="Enter your current name"
              value={oldName}
              onChange={(e) => setOldName(e.target.value)}
            />
            <input
              className='txt1'
              type="text"
              placeholder="Enter your new name"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
            />
            <button
              className="personal-information-button"
              onClick={handleUpdateName}
            >
              Apply Changes
            </button>
          </div>
          <div>
            <h2>Surname: {surname}</h2>
            <input
              className='txt1'
              type="text"
              placeholder="Enter your current surname"
              value={oldSurname}
              onChange={(e) => setOldSurname(e.target.value)}
            />
            <input
              className='txt1'
              type="text"
              placeholder="Enter your new surname"
              value={newSurname}
              onChange={(e) => setNewSurname(e.target.value)}
            />
            <button
              className="personal-information-button"
              onClick={handleUpdateSurname}
            >
              Apply Changes
            </button>
          </div>
          <div>
            <h2>Username: {username}</h2>
            <input
              className='txt1'
              type="text"
              placeholder="Enter your current username"
              value={oldUSername}
              onChange={(e) => setOldUsername(e.target.value)}
            />
            <input
              className='txt1'
              type="text"
              placeholder="Enter your new username"
              value={newUsername}
              onChange={(e) => {
                setNewUsername(e.target.value);
                setUsernameError('');
              }}
            />
            <p>
              <strong>{usernameError}</strong>
            </p>
            <button
              className="personal-information-button"
              onClick={handleUpdateUsername}
              disabled={!validateUsername(newUsername) || !!usernameError}
            >
              Apply Changes
            </button>
          </div>
          <div>
            <h2>Password: </h2>
            <input
              className='txt2'
              type="password"
              placeholder="Enter your old password"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
            />
            <input
              className='txt2'
              type="password"
              placeholder="Enter your new password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
            <p className="error-message">
              {oldPassword === '' && 'Please enter your old password. '}
              {newPassword === '' && 'Please enter a new password.'}
              {newPassword.length > 0 && newPassword.length < 6 && 'Password must be at least 6 characters.'}
            </p>
            <button
              className="personal-information-button"
              onClick={handleUpdatePassword}
              disabled={!validatePassword(newPassword)}
            >
              Apply Changes
            </button>
          </div>
        </div>
        <div className="personal-information-buttons">
          <button className="personal-information-button" onClick={handleDeleteAccount}>
            Delete Account
          </button>
        </div>
      </div>

      {confirmationModal && (
        <div className="modal-overlay">
          <div className="modal">
            <p>{`Are you sure you want to apply changes to ${fieldToUpdate}?: `}</p>
            <button onClick={confirmUpdateField}>Yes</button>
            <button onClick={closeConfirmationModal}>No</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PersonalInformation;