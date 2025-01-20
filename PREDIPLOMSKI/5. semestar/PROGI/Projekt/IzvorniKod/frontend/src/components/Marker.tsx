import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { Icon } from "leaflet";
import { LocalHospital } from "@mui/icons-material";
import { red } from "@mui/material/colors";
import MarkerClusterGroup from "react-leaflet-cluster";

export type customeIcon = {
    iconUrl: any,
    iconSize: number[]
};

const customeIcon = new Icon({
    iconUrl: "https://cdn-icons-png.flaticon.com/128/684/684908.png",
    iconSize: [38, 38]
})

const MapComponent: React.FC = () => {
    const center = {lat: 45.8, lng: 15.971793};
    const zoom = 10;

    const locations = [
        {id: 1, name: 'KBC Osijek', position: {lat: 45.557861, lng: 18.713676}},
        {id: 2, name: 'KBC Rijeka', position: {lat: 45.331938, lng: 14.427058}},
        {id: 3, name: 'KBC Split', position: {lat: 43.503787, lng: 16.457786}},
        {id: 4, name: 'OB Dubrovnik', position: {lat: 42.647721, lng: 18.075879}},
        {id: 5, name: 'OB Varaždin', position: {lat: 46.302635, lng: 16.325343}},
        {id: 6, name: 'OB Zadar', position: {lat: 44.107214, lng: 15.234599}},
        {id: 7, name: 'Hrvatski zavod za transfuzijsku medicinu Zagreb', position: {lat: 45.815994, lng: 15.991180}}
    ];

    return (
        <MapContainer center={center} zoom={zoom} style={{position: 'absolute' ,width: '470px', height: '350px', left: '3%', top: '15%'}}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                // attribution='&copy; OpenStreetMap contributors'
            />
            <MarkerClusterGroup>
                {locations.map((location) => (
                    <Marker key={location.id} position={location.position} icon={customeIcon}>
                        <Popup><LocalHospital sx={{width: "15px", height: "15px", color: 'red'}}/>&nbsp;&nbsp;{location.name}</Popup>
                    </Marker>
                ))}
            </MarkerClusterGroup>
        </MapContainer>
    );
};

export default MapComponent;