import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ErrorResponse, Login } from "../models/Login";
import { AxiosError } from "axios";
import { Button, FormControl, IconButton, InputAdornment, InputLabel, OutlinedInput, TextField } from "@mui/material";
import PersonIcon from '@mui/icons-material/Person';
import LockRoundedIcon from '@mui/icons-material/LockRounded';
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { loginUser } from "../functions/UserFunc";
import { setUserData } from "../functions/LoginFunc";
import '../styles/Login.css'
import axios from "axios";

export function LoginComponent() {
    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [showPassword, setShowPassword] = useState<boolean>(false);
    const [loginFailed, setLoginFailed] = useState<boolean>(false);
    const [submit, setSubmit] = useState<boolean>(false);
    const [error, setError] = useState<string>("");
    const navigate = useNavigate();

    const handleNavigation = () => {
        navigate("/register");
    }

    const clickShowPassword = () => setShowPassword((hide) => !hide);

    const handleMouseEvent = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
    }

    async function handleSubmit(event: any) {
        event.preventDefault();
        setLoginFailed(false);
        setSubmit(true);
        setError("");

        const bloodDonorResponse = await axios.post("/api/login", {
            username: username,
            password: password
        }, {
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        }).catch(function (error) {
            const bloodDonorResponse = error.response;
            if (bloodDonorResponse.status === 401) {
                alert("Incorrect Username and Password");
            } else if (bloodDonorResponse.status === 406) {
                alert("Username does not exist");
            } else {
                alert("Internal application error");
            }
            setSubmit(false);
            console.error("Error:", error.message);
            console.log(error.config);
        });

        if (bloodDonorResponse === undefined) return;

        if (bloodDonorResponse.status === 200) {
            const id = bloodDonorResponse.headers["id"];
            //check if donorId is integer, if not error and return
            if (id === undefined || isNaN(parseInt(id))) {
                alert("Internal application error");
                setSubmit(false);
                console.error("Error: Bad donorId received after login");
                return;
            }

            const type = bloodDonorResponse.headers["type"];
            if (type == "organization") {
                navigate(`/organizationHomepage/${id}`);
            } else if (type == "donor") {
                navigate(`/homepage/${id}`);
            } else {
                alert("Internal application error");
                setSubmit(false);
                console.error("Error: Bad type received after login");
                return;
            }
        }
    }

    return (
        <div className="login">
            <div className="data-login">
                <div className="title-login"><p className="naslov-login"><b>Login</b></p></div>
                <TextField className="username" id="username" label={
                    <div className="user-div"><PersonIcon sx={{ width: "25px", height: "25px" }} />&nbsp;&nbsp;Username</div>
                }
                    onChange={e => setUsername(e.target.value)}
                    size="small"
                />
                <FormControl variant="outlined" size="small">
                    <InputLabel htmlFor="outlined-adornment-password">
                        <div className="user-div"><LockRoundedIcon sx={{ width: "25px", height: "25px" }} />&nbsp;&nbsp;Password</div>
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
                            <div className="user-div"><LockRoundedIcon sx={{ width: "25px", height: "25px" }} />&nbsp;&nbsp;Password</div>
                        }
                    />
                </FormControl>
            </div>
            <div className="error2">
                <div className="title-login">
                    <p className="err">
                        {loginFailed ? 'Wrong username or password.' : ''}
                        {error.length > 0 ? <p className="err">{error}</p> : <></>}
                    </p>
                </div>
            </div>
            <div className="footer2">
                <Button disabled={submit} variant="contained" onClick={handleSubmit}>Login</Button>
                <Button variant="text" onClick={handleNavigation}>Register</Button>
            </div>
        </div>
    );
}