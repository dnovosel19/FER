import { Link } from "react-router-dom";
import { LoginComponent } from "../components/Login";
import '../styles/Login.css';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { Button } from "@mui/material";

export function Login() {
    return (
        <div className="log-in">
            <div className="go-back">
                {/* <Link to="/"><ArrowBackIcon sx={{width: "40px", height: "40px"}} className="arrow"/></Link> */}
                <Link to="/"><Button className="btn" variant="outlined" startIcon={<ArrowBackIcon/>} sx={{color: 'white', bgcolor: 'red', '&:hover': { bgcolor: '', borderColor: 'red', color: 'black', '& svg': {visibility: 'visible'} } }}>Homepage</Button></Link>
            </div>
            <LoginComponent/>
        </div>
    );
}