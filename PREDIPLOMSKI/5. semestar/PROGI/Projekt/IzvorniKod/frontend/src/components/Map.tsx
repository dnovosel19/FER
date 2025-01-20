import React,{useRef,useState,useEffect} from 'react';
import '../styles/Map.css'
interface IMap{
    mapType: google.maps.MapTypeId,
    mapTypeControl?:boolean;
}

type GoogleLatLng=google.maps.LatLng;
type GoogleMap=google.maps.Map;

const Map:React.FC<IMap>=({mapType,mapTypeControl=false})=>{
    
    const ref=useRef<HTMLDivElement>(null);

    const [map,setMap]=useState<GoogleMap>();
    const startMap=():void=>{
        if(!map){
            defaultMapStart();
        }
    };
    useEffect(startMap,[map]);

    const defaultMapStart=():void=>{
        const defaultAddres=new google.maps.LatLng(45.815399,15.966568);//Zagreb def lat long
        initMap(10,defaultAddres);
    };

    const initMap=(zoomLevel:number,addres:GoogleLatLng):void=>{
        if(ref.current){
            setMap(
                new google.maps.Map(ref.current,{
                    zoom:zoomLevel,
                    center: addres,
                    mapTypeControl:mapTypeControl,
                    streetViewControl:false,
                    zoomControl:true,
                    mapTypeId:mapType
                })
            );
        }
    };

    
    return(
        <div className='container_map'>
            <div ref={ref} className='map'>

            </div>
        </div>
    );
};

export default Map;