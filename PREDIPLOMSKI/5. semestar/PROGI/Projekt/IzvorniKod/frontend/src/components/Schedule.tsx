import { Accordion, AccordionDetails, AccordionSummary, Paper, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@mui/material";
import Table from '@mui/material/Table';
import { red } from "@mui/material/colors";
import { create } from "@mui/material/styles/createTransitions";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useEffect, useState } from "react";

function createData(
    name: string,
    place: string,
    address: string,
    workh: string,
    breakt: string,
    dan: string
) {
    return { name, place, address, workh, breakt, dan };
}

const rows = [
    createData('Dubrovnik', 'OB Dubrovnik', 'Dr. Roka Mišetića 2', '09:00 - 12:00', '-', 'Monday'),
    createData('Dubrovnik', 'OB Dubrovnik', 'Dr. Roka Mišetića 2', '08:00 - 12:00', '10:00 - 10:30', 'Thursday'),
    createData('Split', 'KBC Split', 'Spinčićeva ulica 1', '07:30 - 15:00', '13:00 - 13:30', 'Monday'),
    createData('Split', 'KBC Split', 'Spinčićeva ulica 1', '07:30 - 15:00', '13:00 - 13:30', 'Tuesday'),
    createData('Split', 'KBC Split', 'Spinčićeva ulica 1', '07:30 - 19:00', '14:00 - 14:30', 'Wednesday'),
    createData('Split', 'KBC Split', 'Spinčićeva ulica 1', '07:30 - 19:00', '14:00 - 14:30', 'Thursday'),
    createData('Split', 'KBC Split', 'Spinčićeva ulica 1', '07:30 - 15:00', '-', 'Friday'),
    createData('Zadar', 'OB Zadar', 'Ul. Bože Peričića 5', '08:00 - 12:00', '-', 'Tuesday'),
    createData('Zadar', 'OB Zadar', 'Ul. Bože Peričića 5', '14:00 - 19:00', '16:00 - 16:30', 'Wednesday'),
    createData('Zadar', 'OB Zadar', 'Ul. Bože Peričića 5', '08:00 - 12:00', '-', 'Friday'),
    createData('Rijeka', 'KBC Rijeka', 'Krešimirova ulica 42', '08:00 - 15:00', '12:30 - 13:00', 'Monday'),
    createData('Rijeka', 'KBC Rijeka', 'Krešimirova ulica 42', '08:00 - 15:00', '12:30 - 13:00', 'Tuesday'),
    createData('Rijeka', 'KBC Rijeka', 'Krešimirova ulica 42', '08:00 - 19:00', '13:30 - 14:00', 'Wednesday'),
    createData('Rijeka', 'KBC Rijeka', 'Krešimirova ulica 42', '08:00 - 19:00', '13:30 - 14:00', 'Thursday'),
    createData('Rijeka', 'KBC Rijeka', 'Krešimirova ulica 42', '08:00 - 15:00', '12:30 - 13:00', 'Friday'),
    createData('Osijek', 'KBC Osijek', 'Ul. Josipa Huttlera 4', '07:30 - 14:30', '12:00 - 12:30', 'Monday'),
    createData('Osijek', 'KBC Osijek', 'Ul. Josipa Huttlera 4', '12:00 - 19:00', '-', 'Tuesday'),
    createData('Osijek', 'KBC Osijek', 'Ul. Josipa Huttlera 4', '07:30 - 18:30', '13:30 - 14:00', 'Wednesday'),
    createData('Osijek', 'KBC Osijek', 'Ul. Josipa Huttlera 4', '12:00 - 19:00', '-', 'Thursday'),
    createData('Osijek', 'KBC Osijek', 'Ul. Josipa Huttlera 4', '07:30 - 14:30', '12:00 - 12:30', 'Friday'),
    createData('Varaždin', 'OB Varaždin', 'Ul. Ivana Meštrovića 1', '07:30 - 11:00', '-', 'Monday'),
    createData('Varaždin', 'OB Varaždin', 'Ul. Ivana Meštrovića 1', '07:30 - 13:00', '-', 'Wednesday'),
    createData('Varaždin', 'OB Varaždin', 'Ul. Ivana Meštrovića 1', '07:30 - 13:00', '-', 'Thursday'),
    createData('Varaždin', 'OB Varaždin', 'Ul. Ivana Meštrovića 1', '07:30 - 11:00', '-', 'Friday'),
    createData('Zagreb', 'HZTM', 'Petrova ulica 3', '07:30 - 19:00', '13:00 - 13:30', 'Monday'),
    createData('Zagreb', 'HZTM', 'Petrova ulica 3', '07:30 - 19:00', '-', 'Tuesday'),
    createData('Zagreb', 'HZTM', 'Petrova ulica 3', '07:30 - 19:00', '13:00 - 13:30', 'Wednesday'),
    createData('Zagreb', 'HZTM', 'Petrova ulica 3', '07:30 - 19:00', '-', 'Thursday'),
    createData('Zagreb', 'HZTM', 'Petrova ulica 3', '07:30 - 19:00', '13:00 - 13:30', 'Friday'),
    createData('Zagreb', 'HZTM', 'Petrova ulica 3', '07:30 - 15:00', '-', 'Saturday'),
    createData('Zagreb', 'HZTM', 'Petrova ulica 3', '07:30 - 15:00', '-', 'Sunday'),
];

export function ScheduleComponent() {
    const [expandedAccordion, setExpandedAccordion] = useState<string | null>(null);
    const [days, setDays] = useState<string[]>([]);
    const [dates, setDates] = useState<string[]>([]);

    useEffect(() => {
        const updateDates = () => {
            const todayIndex = new Date().getDay()-1;
            const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

            const reorderedDays = [...daysOfWeek.slice(todayIndex), ...daysOfWeek.slice(0, todayIndex)];
            setDays(reorderedDays);

            const currentDate = new Date();
            const formattedDates = reorderedDays.map((day, index) => {
                const date = new Date(currentDate);
                date.setDate(currentDate.getDate() + index);
                const options: Intl.DateTimeFormatOptions = {year: "numeric", month: "numeric", day: "numeric"};
                return date.toLocaleDateString("en-Us", options);
            });

            setDates(formattedDates);
        };

        updateDates();
        const intervalId = setInterval(updateDates, 60000);
        return () => clearInterval(intervalId);
    }, []);

    const handleOnClick = (day: string) => {
        if (expandedAccordion === day) {
            setExpandedAccordion(null);
        } else {
            setExpandedAccordion(day);
        }
    };

    return (
        <div style={{marginTop: '10px', marginBottom: '20px'}}>
            {days.map((day, index) => (
                <Accordion
                    key={day}
                    expanded={expandedAccordion === day} 
                    onChange={() => handleOnClick(day)}
                    style={{marginBottom: index !== days.length - 1 ? '15px' : '0', marginLeft: '50px', marginRight: '50px', borderRadius: '20px', overflow: 'hidden'}}
                >
                    <AccordionSummary 
                        expandIcon={<ExpandMoreIcon/>} 
                        aria-controls={`${day}-content`} 
                        id={`${day}-header`} 
                        style={{
                            backgroundColor: expandedAccordion === day ? 'red' : '#d6bbbb', 
                            color: expandedAccordion === day ? 'white' : 'inherit'
                        }}
                    >
                        <Typography style={{marginLeft: '70px'}}>{day} - {dates[index]}</Typography>
                    </AccordionSummary>
                    <AccordionDetails style={{ maxHeight: '300px', overflowY: 'auto', overflowX: 'auto', marginLeft: '100px', marginRight: '100px' }}>
                     <Typography>
                         <TableContainer component={Paper}>
                             <Table sx={{ minWidth: 1000}} aria-label="simple table">
                                 <TableHead>
                                     <TableRow>
                                         <TableCell align="center"><b>City</b></TableCell>
                                         <TableCell align="center"><b>Place</b></TableCell>
                                         <TableCell style={{color: "black"}} align="center"><b>Address</b></TableCell>
                                         <TableCell style={{color: "black"}} align="center"><b>Working hours</b></TableCell>
                                         <TableCell style={{color: "black"}} align="center"><b>Break</b></TableCell>
                                     </TableRow>
                                 </TableHead>
                                 <TableBody>
                                     {rows
                                        .filter(row => row.dan === days[index])
                                        .map((row) => (
                                            <TableRow key={row.name} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                                <TableCell component="th" scope="row" align="center">{row.name}</TableCell>
                                                <TableCell align="center">{row.place}</TableCell>
                                                <TableCell align="center">{row.address}</TableCell>
                                                <TableCell align="center">{row.workh}</TableCell>
                                                <TableCell align="center">{row.breakt}</TableCell>
                                            </TableRow>
                                        ))}
                                 </TableBody>
                             </Table>
                         </TableContainer>
                     </Typography>

                    </AccordionDetails>
                </Accordion>
            ))}
        </div>
    );
}