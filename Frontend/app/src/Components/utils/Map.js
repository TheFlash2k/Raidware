// import React from 'react';
// import { MapContainer, TileLayer, Marker } from 'react-leaflet';
// import { Icon } from 'leaflet';
// import 'leaflet/dist/leaflet.css';

// // Grey icon for the marker
// const greyIcon = new Icon({
//   iconUrl: 'https://cdn.jsdelivr.net/gh/pointhi/leaflet-color-markers@master/img/marker-icon-grey.png',
//   iconSize: [25, 41],
//   iconAnchor: [12, 41],
//   popupAnchor: [1, -34],
// });

// function Map({ coordinates }) {
//     console.log("Inside the map: ");
//     console.log(coordinates);
//   return (
//     <div>
//         <MapContainer center={[0, 0]} zoom={2} style={{ height: '800px', width: '100%' }}>
//         <TileLayer
//             url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png"
//             attribution="Map data © OpenStreetMap contributors"
//         />
//         {coordinates.map((location, index) => (
//             <Marker key={index} position={[location.lat, location.lon]} icon={greyIcon} />
//         ))}
//         </MapContainer>
//     </div>
//   );
// }

// export default Map;

import React from 'react';
import { MapContainer, Marker, TileLayer, Popup, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const LeafletMap = ({ coordinates }) => {
  const worldGeoURL = 'https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson';

  return (
    <div style={{ width: '100%', height: '800px', backgroundColor: 'grey' }}>
      <MapContainer center={[0, 0]} zoom={1} style={{ width: '100%', height: '100%' }}>
        <TileLayer
          url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png"
          attribution="Map data © OpenStreetMap contributors"
        />
        <GeoJSON
          data={worldGeoURL}
          style={{ fill: '#1a1a1c', stroke: '#575757' }}
        />
        {coordinates && coordinates.map((location, index) => (
          <Marker key={index} position={[location.coordinates.lat, location.coordinates.lon]}>
            <Popup>
              <span style={{ fontWeight: 'bold', color: 'white' }}>{location.countryName}</span>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default LeafletMap;
