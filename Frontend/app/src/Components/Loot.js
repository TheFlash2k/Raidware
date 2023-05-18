import { useState, useEffect } from "react";
import rd01 from './resources/rd-01 1.png';
import rd02 from './resources/rd-01 inverted 1.png';
import rd03 from './resources/rd-01.png';
import rd04 from './resources/rd-01 inverted.png';
import axios from "axios";
import './styles/Loot.css';
import { showPopup, hidePopup } from "./utils/Popup";
import './styles/Popup.css'


export default function Loot() {

    const [loots, setLoots] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        hidePopup();
        const url = localStorage.getItem('url') + "/loot";

        axios.get(url, {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            }
        }).then((response) => {
            setLoots(response.data.loot);
            console.log(response.data);
        }).catch((error) => {
            console.log(error);
        });
    }, []);

    const handleDark = () => {
      hidePopup();
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
    
        const handleNav = () => {
          hidePopup();
            // const mySection = document.getElementById('mySection');
            // mySection.classList.toggle('left-position');
    
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
            // content.classList.toggle("stretched");
            // stretchButton.classList.toggle("left-position");
        }
    
        const handleChangeDark = () => {
            const body = document.body;
            body.classList.toggle("dark-mode");
        }

        const handleCreateLoot = () => {
          hidePopup();
        const createFormPage = document.getElementById('createFormPage');
        createFormPage.classList.toggle('top-position');
        }

    return(
        <div class="main">
        <div class="form-page" id="createFormPage">
          <div class="logo-section-light show" id="div5">
            <img
              src={rd03}
              alt="logo"
              class="logo-create-Light"
              id="createLogoLight"
            />
          </div>
          <div class="logo-section-dark hide" id="div6">
            <img
              src={rd04}
              alt="logo"
              class="logo-create-dark"
              id="createLogoDark"
            />
          </div>
          <form class="form">
            <div class="form-scroll">
              <input class="input-create-loot" type="text" placeholder="Name" required="required" />
              <select name="Type" id="protocol">
                <option value="Password">Password</option>
                <option value="Hash">Hash</option>
              </select>
            <input class="input-create-loot" type="text" placeholder="Content" required="required" />
            <input class="input-create-loot" type="text" placeholder="Description" required="required" />
            <input type="submit" value="Submit" class="sub-loot" />
            </div>
          </form>
        </div>

        <div class="toggle-container">
          <input onClick={handleDark} onChange={handleChangeDark} type="checkbox" id="toggle" class="toggle-checkbox" />
          <label for="toggle" class="toggle-label">
            <span class="toggle-inner"><i class="fa-solid fa-sun"></i></span>
            <span class="toggle-switch"><i class="fa-solid fa-moon"></i></span>
          </label>
        </div>
        <div class="logo-light show" id="div3">
          <img src={rd01} alt="LOGO" />
        </div>
        <div class="logo-dark hide" id="div4">
          <img src={rd02} alt="LOGO" />
        </div>
        <div class="Loots">
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
            <div class="error-popup" id="err-popup">
                  <p>Error:&nbsp;</p>
                  <button onClick={hidePopup}>
                      <i class="fa-solid fa-xmark"></i>
                  </button>
                  <div>{errorMessage}</div>
              </div>
              <div class="loot">
                <h2 class="heading" id="mySection">Loot</h2>
                <button class="create" id="create">Add Loot</button>
              </div>
              <div class="loot-menu">
                <div class="id loot-menu-child">
                  ID &nbsp;<i class="fa-solid fa-up-down"></i>
                </div>
                <div class="name loot-menu-child">
                  Name &nbsp;<i class="fa-solid fa-up-down"></i>
                </div>
                <div class="type loot-menu-child">
                  Type &nbsp;<i class="fa-solid fa-up-down"></i>
                </div>
                <div class="content- loot-menu-child">
                  Content &nbsp;<i class="fa-solid fa-up-down"></i>
                </div>
                <div class="description loot-menu-child">
                  Description &nbsp;<i class="fa-solid fa-up-down"></i>
                </div>
                <div class="operations loot-menu-child">
                  Operations
                </div>
              </div>
              <div class="loot-items">
                <div class="loot-items-scroll">
                  { loots.map((loot) => (
                  <div class="dummy" key={loot.id}>
                    <div class="dummy-child">{loot.id}</div>
                  <div class="dummy-child">{loot.name}</div>
                  <div class="dummy-child">{loot.type}</div>
                  <div class="dummy-child">{loot.value}</div>
                  <div class="dummy-child" >{loot.description}</div>
                    <div class="dummy-child icons-dummy">
                      <div class="edit-dummy dummy-icon">
                        <i class="fa-solid fa-pen-to-square fa-lg"></i>
                      </div>
                      <div class="delete-dummy dummy-icon">
                        <i class="fa-solid fa-trash fa-lg"></i>
                      </div>
                    </div>
                  </div>
                    ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
    )
}