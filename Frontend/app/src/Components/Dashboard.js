import React, { useEffect, useState } from 'react';
import rd01 from './resources/rd-01 1.png';
import rd02 from './resources/rd-01 inverted 1.png';
import rd03 from './resources/rd-01.png';
import dark_logo from './resources/rd-01 inverted.png';
import './styles/Dashboard.css'
import axios from "axios";
import { Chart } from "react-google-charts";
import { ComposableMap, Geographies, Geography, Marker, ZoomableGroup, ZoomControl, Map } from 'react-simple-maps';
const worldGeoURL = 'https://raw.githubusercontent.com/deldersveld/topojson/master/world-countries.json';

export default function Dashboard() {

  const [user, setUser] = useState(0);
  const [sessions, setSessions] = useState(0);
  const [listeners, setListeners] = useState(0);
  const [backgroundColor, setBackgroundColor] = useState('white');
  const [fontColor, setFontColor] = useState('black');
  const [darkMode, setDarkMode] = useState(false);
  const [coordinates, setCoordinates] = useState([{"name" : "", "coordinates" : [0, 0]}]);

  const [showPopup, setShowPopup] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState(null);

  const togglePopup = (location) => {
    setShowPopup(!showPopup);
    setSelectedLocation(location);
  };

  const changeBackgroundColor = (color) => {
    setBackgroundColor(color); // Change the background color to yellow
  };

  const options = {
    title: "Sessions OS",
    pieHole: 0.3,
    is3D: false,
    pieStartAngle: 100,
    pieSliceTextStyle: {
      color: fontColor,
    },
    legend: {
      textStyle : {
        color: fontColor
      }
    },
    backgroundColor: backgroundColor,
    titleTextStyle: { 
      color: fontColor
    }
  };

  const handleDark = () => {

    const div1 = document.getElementById("div1");
    const div2 = document.getElementById("div2");
    const div3 = document.getElementById("div3");
    const div4 = document.getElementById("div4");

    if (div3.classList.contains("show")) {
      div3.classList.remove("show");
      div3.classList.add("hide");
      div4.classList.remove("hide");
      div4.classList.add("show");
    }
    else {
      div3.classList.remove("hide");
      div3.classList.add("show");
      div4.classList.remove("show");
      div4.classList.add("hide");
    }

    if (div1.classList.contains("visible")) {
        div1.classList.remove("visible");
        div1.classList.add("hidden");
        div2.classList.remove("hidden");
        div2.classList.add("visible");
      } else {
        div1.classList.remove("hidden");
        div1.classList.add("visible");
        div2.classList.remove("visible");
        div2.classList.add("hidden");
      }
    }

    const handleChangeDark = () => {

      
      const body = document.body;
      
      if (body.classList.contains("dark-mode")) {
        setFontColor('black');
        setBackgroundColor('white');
      }
      else {
        setFontColor('white');
        setBackgroundColor('#23242a');
      }
      body.classList.toggle("dark-mode");
  }

  const handleNav = () => {
    const navbar = document.getElementById("navbar");
    navbar.classList.toggle("stretched");
    if (navbar.classList.contains("stretched")) {
        const mySection = document.getElementById('mySection');
        mySection.style.left = '15px'
    }
    else {
        const mySection = document.getElementById('mySection');
        mySection.style.left = '120px'
    }
  }

  const GET = (_obj, setterFunc, __endpoint = null) => {
    var url = localStorage.getItem('url') + "/";
    if(__endpoint === null) {
      url +=  _obj;
    }
    else {
      url += __endpoint;
    }
    const token = localStorage.getItem('token');
    axios.get(url, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    }).then((response) => {
        setterFunc(response.data[_obj].length);
    }
    ).catch((error) => {console.log("Error", error);});
  }

  const getUsers = () => { GET('users', setUser) }
  const getSessions = () => { GET('sessions', setSessions) }
  const getListeners = () => { GET('listeners', setListeners, 'enabled') }

  const [osData, setOsData] = useState([
    ['OS', 'Sessions'],
    ['Windows', 0],
    ['MacOS', 0],
    ['Linux', 0]
  ]);

  const getOS = () => {
    var url = localStorage.getItem('url') + "/sessions";
    const token = localStorage.getItem('token');
    axios.get(url, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    }).then((response) => {
        var windows = 0;
        var macos = 0;
        var linux = 0;
        const sessions = response.data.sessions;
        sessions.forEach((session) => {
          if(session.OS.toLowerCase().includes('windows')) {
            console.log("==> Windows");
            windows += 1;
          }
          else if(session.OS.toLowerCase().includes('macos')) macos += 1;
          else linux += 1;
        });
        const _osData = [
          ['OS', 'Sessions'],
          ['Windows', windows],
          ['MacOS', macos],
          ['Linux', linux]
        ]
        console.log(_osData);
        setOsData(_osData);
    }).catch((error) => {console.log("Error", error);});
  }

  const getMapLocation = () => {
    // Make a get request to /stats to get the location of the listeners
    var url = localStorage.getItem('url') + "/stats";
    const token = localStorage.getItem('token');
    axios.get(url, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    }).then((response) => {
      console.log("Response from MAP: ");
      console.log(response.data);

      // Iterate over the dictionary in response.data:
      var coords = [];
      for(const [key, value] of Object.entries(response.data)) {
        coords.push({
          name: value.country,
          coordinates: [value.longitude, value.latitude]
        });
      }
      console.log(coords);
      setCoordinates(coords);

    }).catch((error) => {console.log("Error", error);});
  }

  const handleMarkerClick = (location) => {
    console.log("Marker clicked: ");
  }

  useEffect(() => {

    if(localStorage.getItem('token') === null || localStorage.getItem('url') === null) {
      window.location.replace("/login");
    }

    getUsers();
    getSessions();
    getListeners();
    getOS();
    getMapLocation();
  }, [coordinates]);

  

  return (
    <div>
      <div class="toggle-container">
        <input onClick={handleDark} onChange={handleChangeDark} type="checkbox" id="toggle" class="toggle-checkbox" />
        <label for="toggle" class="toggle-label">
        <span class="toggle-inner"><i class="fa-solid fa-sun"></i></span>
        <span class="toggle-switch"><i class="fa-solid fa-moon"></i></span>
        </label>
      </div>
    <div class="logo-light show" id="div3"><img src={rd01} alt="LOGO" /></div>
    <div class="logo-dark hide" id="div4"><img src={rd02} alt="LOGO" /></div>
    
    <div class="dashboards">
      <div class="container">
        <div class="navbar" id="navbar">
          <div class="navbar-logo-light visible" id="div1">
            <img src={rd01} alt="LOGO" />
          </div>
          <div class="navbar-logo-dark hidden" id="div2">
            <img src={rd02} alt="LOGO" />
          </div>
          <button onClick={handleNav} id="stretchButton" class="stretch-button">
            <span class="arrow-icon"></span>
          </button>
          <div class="a-tags">
              <a href="/"><i class="fa-solid fa-chart-line"></i>&nbsp; &nbsp;Dashboard</a>
              <a href="/listeners"><i class="fa-solid fa-headphones"></i> &nbsp; &nbsp;Listeners</a>
							<a href="/sessions"><i class="fa-solid fa-briefcase"></i> &nbsp; &nbsp; Session</a>
							<a href="/agents"><i class="fa-solid fa-users"></i> &nbsp; &nbsp; Agents</a>
							<a href="/loot"><i class="fa-solid fa-coins"></i> &nbsp; &nbsp; Loot</a>
							<a href="/users"><i class="fa-solid fa-user"></i> &nbsp; &nbsp; Users</a>
							<a href="/logout" className="logout"><i className="fa-solid fa-right-from-bracket"></i> &nbsp; &nbsp; Log-out</a>
          </div>
        </div>
        <div class="content" id="content">
          <div class="dash">
            <h2 class="heading" id="mySection">Dashboard</h2>
          </div>
          <div class="dashboard">
              <div class="analatics">
                <div class="total-enabled-listner card">
                  <div class="enabled-listner-icon icon">
                    <i class="fa-solid fa-headphones"></i>
                  </div>
                  <p>Total Enabled Listeners</p>
                  <h4>{listeners}</h4><hr></hr>
                  <p class="card-status">Just Updated</p>
                </div>

                <div class="sessions card">
                  <div class="session-icon icon">
                    <i class="fa-solid fa-briefcase"></i>
                  </div>
                  <p>Sessions</p>
                  <h4>{sessions}</h4><hr></hr>
                  <p class="card-status">Just Updated</p>
                </div>
                
                <div class="total-user card">
                  <div class="total-user-icon icon">
                    <i class="fa-solid fa-user"></i>
                  </div>
                  <p>Users</p>
                  <h4 class="user-data">{user}</h4><hr></hr>
                  {/* <!-- <p class="card-status user-status"><span>+3%</span> than last Month</p> --> */}
                  <p class="card-status">Just Updated</p>
                </div>

              </div>
            
              <div class="map">
                <div class="total-user-map">
                <div style={{ width: '100%', height: '800px', backgroundColor: backgroundColor }}>
                  <ComposableMap projection="geoMercator" style={{ width: '100%', height: '100%' }}>
      <ZoomableGroup zoom={1} center={[0, 0]}>
        <Geographies geography={worldGeoURL}>
          {({ geographies }) =>
            geographies.map((geo) => (
              <Geography key={geo.rsmKey} geography={geo} fill="#1a1a1c" stroke="#575757" />
            ))
          }
        </Geographies>

                      {coordinates &&
                        coordinates.map((location) => (
                          <Marker key={location.id} coordinates={[location.coordinates[0], location.coordinates[1]]}>
                                <a href="#" onClick={() => togglePopup(location)}>
                              <circle r={2} fill="#F00" />
                            </a>
                          </Marker>
                        ))}

                      {showPopup && selectedLocation && (
                        <div className="popup-container">
                          <div className="popup">
                            <h3>{selectedLocation.name}</h3>
                            <button className="close-button" onClick={togglePopup}>
                              Close
                            </button>
                          </div>
                        </div>
                      )}
                    </ZoomableGroup>
                  </ComposableMap>
                </div>

                </div>
                <div class="pie-chart">
                <Chart
                    chartType="PieChart"
                    width="100%"
                    height="500px"
                    data={osData}
                    options={options}
                  />
                </div>
              </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  );
}