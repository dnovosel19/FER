import { Button, FormControl, IconButton, InputAdornment, InputLabel, MenuItem, OutlinedInput, TextField } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Register, RegisterOrganization, registerOrganization } from "../functions/RegisterFunc";
import PersonIcon from '@mui/icons-material/Person';
import PinIcon from '@mui/icons-material/Pin';
import { AxiosError } from "axios";
import { ErrorResponse } from "../models/Login";
import '../styles/Register.css'
import LockRoundedIcon from '@mui/icons-material/LockRounded';
import { Phone, Visibility, VisibilityOff } from "@mui/icons-material";
import { setUserData } from "../functions/LoginFunc";

export function RegisterComponentOrganization() {
    const [adminUsername, setAdminUsername] = useState<string>("");
    const [adminPassword, setAdminPassword] = useState<string>("");
    const [adminName, setAdminName] = useState<string>("");
    const [adminSurname, setAdminSurname] = useState<string>("");
//     const [location, setLocation] = useState<string>("");
//     const [organizationType, setOrganizationType] = useState<string>("");
    const [naziv, setNaziv] = useState<string>("");
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

    const valid = (): string[] => {
        let error: string[] = [];
        if (!adminName) error.push("You must enter your name");
        if (!adminUsername) error.push("You must enter your username");
        if (adminUsername.length < 6 || adminUsername.length > 20) error.push("Username must contain more than 6 and less than 20 characters");
        if (adminPassword.length < 6) error.push("Password must contain at least 6 characters");
        if (adminPassword !== passwordAgain) error.push("Passwords don't match");

        return error;
    }

    const clickShowPassword = () => setShowPassword((hide) => !hide);

    const handleMouseEvent = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
    }

    const handleSubmit = (e: any) => {
        e.preventDefault();
        setRegisterFailed(false);
        let errorMessage: string[] = valid();

        console.log('Password:', adminPassword);
        console.log('Password Again:', passwordAgain);
        if (errorMessage.length !== 0) {
            setError(errorMessage);
        } else {
            setSubmit(true);
            setError([]);
            const data: RegisterOrganization = {
                adminUsername: adminUsername,
                adminPassword: adminPassword,
                adminName: adminName,
                adminSurname: adminSurname,
                //TODO - organizationType dropdown menu, location (longitude/latitude picker), remove placeholders
                locationId: 1, //placeholder
                organizationTypeId: 1, //placeholder
                naziv: naziv
            }
            registerOrganization(data).then(e => {
                setUserData(e)
                navigate('/loginOrganization');
            }).catch((e: AxiosError<ErrorResponse>) => {
                setSubmit(false);
                if (e.response === undefined) {
                    setRegisterFailed(true);
                    return;
                }
                errorMessage.push(e.response.data.errorMessage)
                setError(errorMessage)
            })
        }
    }
    return (
        <div className="register2">
            <div className="form-reg-organization">
                <div className="title-reg"><p className="naslov-reg"><b>Register</b></p></div>
                <TextField className="ime" id="name" label={<span className="user-div"><PersonIcon sx={{ width: "25px", height: "25px" }} />&nbsp;&nbsp;Name *</span>}
                    onChange={(e) => setAdminName(e.target.value)} size="small" required={true} InputLabelProps={{ required: false }} />
                <TextField className="ime" id="username" label={<span className="user-div"><PersonIcon sx={{ width: "25px", height: "25px" }} />&nbsp;&nbsp;Username *</span>}
                    onChange={(e) => setAdminUsername(e.target.value)} size="small" required={true} InputLabelProps={{ required: false }} />
                <TextField className="ime" id="surname" label={<span className="user-div"><PersonIcon sx={{ width: "25px", height: "25px" }} />&nbsp;&nbsp;Surname *</span>}
                    onChange={(e) => setAdminSurname(e.target.value)} size="small" required={true} InputLabelProps={{ required: false }} />
                <TextField className="ime" id="naziv" label={<span className="user-div"><PersonIcon sx={{ width: "25px", height: "25px" }} />&nbsp;&nbsp;Title *</span>}
                    onChange={(e) => setNaziv(e.target.value)} size="small" required={true} InputLabelProps={{ required: false }} />
                <div className="name-div">
                    <FormControl variant="outlined" size="small" className="text-field">
                        <InputLabel htmlFor="outlined-adornment-password">
                            <div className="text-div"><LockRoundedIcon sx={{ width: "25px", height: "25px" }} />&nbsp;&nbsp;Password</div>
                        </InputLabel>
                        <OutlinedInput
                            size="small" id="outlined-adornment-password" type={showPassword ? 'text' : 'password'}
                            onChange={(e) => setAdminPassword(e.target.value)}
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
               {error.map((errorMessage: string, index: number) => (
                   <div className="title-reg" key={index}>
                       <p className="err">{errorMessage}</p>
                   </div>
               ))}
               <div className="title-reg">
                   <p className="err">
                       {registerFailed ? "Warning! Error." : ""}
                   </p>
               </div>
           </div>

            <div className="footer2">
                <Button variant="text" onClick={handleNavigation}>Login</Button>
                <Button variant="contained" disabled={submit} onClick={handleSubmit}>Register</Button>
            </div>
        </div>
    );
}
