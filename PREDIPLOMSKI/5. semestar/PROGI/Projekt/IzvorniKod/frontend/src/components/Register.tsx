import { Button, FormControl, IconButton, InputAdornment, InputLabel, MenuItem, OutlinedInput, TextField } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Register, jeBroj, registerUser } from "../functions/RegisterFunc";
import PersonIcon from '@mui/icons-material/Person';
import PinIcon from '@mui/icons-material/Pin';
import { AxiosError } from "axios";
import { ErrorResponse } from "../models/Login";
import '../styles/Register.css'
import LockRoundedIcon from '@mui/icons-material/LockRounded';
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { setUserData } from "../functions/LoginFunc";

export function RegisterComponent() {
    const [name, setName] = useState<string>("");
    const [surname, setSurname] = useState<string>("");
    const [username, setUsername] = useState<string>("");
    const [oib, setOib] = useState<string>("");
    const [bloodType, setBloodType] = useState<string>("");
    const [error, setError] = useState<string[]>([]);
    const [registerFailed, setRegisterFailed] = useState<boolean>(false);
    const [submit, setSubmit] = useState<boolean>(false);
    const [password, setPassword] = useState<string>("");
    const [passwordAgain, setPasswordAgain] = useState<string>("");
    const [showPassword, setShowPassword] = useState<boolean>(false);
    const navigate = useNavigate();

    const handleNavigation = () => {
        navigate('/login');
    }
    const handleNavigationForOrganization = () => {
        navigate('/registerOrganization');
    }

    const valid = (): string[] => {
        let error: string[] = [];
        if (!name) error.push("You must enter your name");
        if (!surname) error.push("You must enter your surname");
        if (!username) error.push("You must enter your username");
        if (6 > username.length) error.push("Username must contain more than 6 characters");
        if (username.length > 20) error.push("Username must contain less than 20 characters");
        if (oib.length != 11 || !jeBroj(oib)) error.push("PIN must contain 11 numbers");
        if (bloodType == "") error.push("Choose your blood type");
        if (password.length < 6) error.push("More characters required for password");
        if (password !== passwordAgain) error.push("Passwords don't match");
        return error;
    }

    const handleBloodType = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setBloodType(value);
    }

    const clickShowPassword = () => setShowPassword((hide) => !hide);

    const handleMouseEvent = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
    }

   const handleSubmit = (e: any) => {
       e.preventDefault();
       setRegisterFailed(false);
       let errorMessage: string[] = valid();

       if (errorMessage.length !== 0) {
           setError(errorMessage);
       } else {
           setSubmit(true);
           setError([]);
           const data: Register = {
               name: name,
               surname: surname,
               username: username,
               oib: oib,
               password: password,
           };

           console.log("Sending registration request with data:", data);

           registerUser(data)
              .then((response) => {
                  if (response.status >= 200 && response.status < 300) {
                      console.log("Registration successful. Response:", response);
                      setUserData(response);

                      const donorId = response.data.id?.id;

                      if (donorId) {
                          console.log("Donor ID:", donorId);
                          navigate(`/homepage/${donorId}`);
                      } else {
                          console.error("Donor ID is undefined or null");
                      }
                  } else {
                      console.error("Unexpected status:", response.status);
                      setRegisterFailed(true);
                  }
              })

               .catch((e: AxiosError<ErrorResponse>) => {
                   console.error("Registration failed. Error response:", e);

                   if (e.response === undefined) {
                       console.error("Server did not respond with details.");
                       setRegisterFailed(true);
                       return;
                   }

                   console.error("Error status:", e.response.status);
                   console.error("Error data:", e.response.data);

                   errorMessage.push(e.response.data.errorMessage);
                   setError(errorMessage);
               })
               .finally(() => {
                   setSubmit(false);
               });
       }
   };

return (
        <div className="register2">
            <div className="form-reg">
                <div className="title-reg"><p className="naslov-reg"><b>Register</b></p></div>
                <TextField className="ime" id="name" label="Name" onChange={(e) => setName(e.target.value)} size="small" required={true} />
                <TextField className="ime" id="surname" label="Surname" onChange={(e) => setSurname(e.target.value)} size="small" required={true} />
                <TextField className="username" id="username" label={<span className="user-div"><PersonIcon sx={{ width: "25px", height: "25px" }} />&nbsp;&nbsp;Username *</span>}
                    onChange={(e) => setUsername(e.target.value)} size="small" required={true} InputLabelProps={{ required: false }} />
                <TextField className="ime" id="oib" label={<span className="user-div"><PinIcon sx={{ width: "25px", height: "25px" }} />&nbsp;&nbsp;PIN *</span>}
                    onChange={(e) => setOib(e.target.value)} size="small" required={false} />
                <TextField className="blood-type" id="bloodType" select label="Blood type" value={bloodType} onChange={handleBloodType} variant="standard" required={true}>
                    {["0+", "0-", "AB+", "AB-", "A+", "A-", "B+", "B-"].map((value: string) => (
                        <MenuItem key={value} value={value}>{value}</MenuItem>
                    ))}
                </TextField>

                <div className="name-div">
                    <FormControl variant="outlined" size="small" className="text-field">
                        <InputLabel htmlFor="outlined-adornment-password">
                            <div className="text-div"><LockRoundedIcon sx={{ width: "25px", height: "25px" }} />&nbsp;&nbsp;Password</div>
                        </InputLabel>
                        <OutlinedInput
                            size="small" id="outlined-adornment-password" type={showPassword ? 'text' : 'password'}
                            onChange={(e) => setPassword(e.target.value)}
                            endAdornment={
                                <InputAdornment position='end'>
                                    <IconButton onClick={clickShowPassword} onMouseDown={handleMouseEvent} edge="end">
                                        {showPassword ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                </InputAdornment>
                            }
                            label={
                                <div className="text-div"><LockRoundedIcon sx={{ width: "25px", height: "25px" }} />&nbsp;&nbsp;Password</div>
                            }
                        />
                    </FormControl>

                    <div className="divider-div" />
                    <TextField className="text-field" id="password-again" label={
                        <span className="text-div">Re-enter password *</span>
                    } type="password" onChange={(e) => setPasswordAgain(e.target.value)} size="small" required={true} InputLabelProps={{ required: false }}
                    />
                </div>
            </div>
            <div className="error-reg">
                {[...error].map((errorMessage: string, key: number) =>
                    <div className="title-reg">
                        <p className="err" key={key}>{errorMessage}</p>
                    </div>)}
                <div className="title-reg">
                    <p className="err">
                        {registerFailed ? "Registration failed. Try again." : ""}
                    </p>
                </div>
            </div>
            <div className="footer2">
                <Button variant="text" onClick={handleNavigation}>Login</Button>
                <Button variant="contained" disabled={submit} onClick={handleSubmit}>Register</Button>
                <div className="organization"><Button variant="text" onClick={handleNavigationForOrganization}>Register as organization</Button></div>

            </div>
        </div>
    );
}