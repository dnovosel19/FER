import { Link } from "react-router-dom";
import { ScheduleComponent } from "../components/Schedule";
import { Button } from "@mui/material";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import '../styles/MainP.css';
import { useEffect, useState } from "react";
import AccessTimeIcon from '@mui/icons-material/AccessTime';

export function Schedule() {
    const currentDate = new Date();
    const formattedDate = currentDate.toLocaleDateString();
    const futureDate = new Date(currentDate);
    futureDate.setDate(currentDate.getDate() + 6);
    const formattedFuture = futureDate.toLocaleDateString();

    const [currentTime, setCurrentTime] = useState<Date>(new Date());

    useEffect(() => {
        const timerId = setInterval(() => tick(), 1000);
        return () => {
            clearInterval(timerId);
        };
    }, []);

    const tick = () => {
        setCurrentTime(new Date());
    };

    return(
        <div className="schedule">
            <h2 className="rasp" style={{color: 'blue', fontSize: '25px'}}>Weekly blood donation schedule {formattedDate} - {formattedFuture}
                <span className="vrijeme" style={{color: 'black'}}><AccessTimeIcon sx={{width: '20px', height: '20px', color: 'black'}}/>&nbsp;{currentTime.toLocaleTimeString()}</span>
            </h2>
            <ScheduleComponent/>
            <Link to="/"><Button className="schbtn" variant="outlined" startIcon={<ArrowBackIcon/>} sx={{color: 'white', bgcolor: 'blue', '&:hover': { bgcolor: '', borderColor: 'red', color: 'black', '& svg': {visibility: 'visible'} } }}>Homepage</Button></Link>
        </div>
    );
}