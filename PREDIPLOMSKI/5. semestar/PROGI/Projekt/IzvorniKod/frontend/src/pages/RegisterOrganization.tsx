import { Link } from "react-router-dom";
import { RegisterComponentOrganization } from "../components/RegisterOrganization";
import '../styles/Register.css'
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { Button } from "@mui/material";

export function RegisterOrganization() {
    return (
        <div className="register">
            <div className="go-back1">
                <Link to="/"><Button variant="outlined" startIcon={<ArrowBackIcon/>} sx={{color: 'white', bgcolor: 'red', '&:hover': { bgcolor: '', borderColor: 'red', color: 'black', '& svg': {visibility: 'visible'} } }}>Homepage</Button></Link>
            </div>
            <RegisterComponentOrganization/>
        </div>
    );
}