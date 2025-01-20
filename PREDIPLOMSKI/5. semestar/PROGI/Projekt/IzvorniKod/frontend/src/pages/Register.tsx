import { Link } from "react-router-dom";
import { RegisterComponent } from "../components/Register";
import '../styles/Register.css'
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { Button } from "@mui/material";

export function Register() {
    return (
        <div className="register">
            <div className="go-back1">
                {/* <Link to="/"><ArrowBackIcon sx={{width: "40px", height: "40px"}} className="arrow"/></Link> */}
                <Link to="/"><Button variant="outlined" startIcon={<ArrowBackIcon/>} sx={{color: 'white', bgcolor: 'red', '&:hover': { bgcolor: '', borderColor: 'red', color: 'black', '& svg': {visibility: 'visible'} } }}>Homepage</Button></Link>
            </div>
            <RegisterComponent/>
        </div>
    );
}