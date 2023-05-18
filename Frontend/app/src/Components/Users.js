import { useState, useEffect } from "react";
import rd01 from './resources/rd-01 1.png';
import rd02 from './resources/rd-01 inverted 1.png';
import rd03 from './resources/rd-01.png';
import rd04 from './resources/rd-01 inverted.png';
import './styles/Users.css';
import axios from "axios";
import { showPopup, hidePopup } from "./utils/Popup";
import './styles/Popup.css'


export default function Users() {

  const [users, setUsers] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    hidePopup();

    if(localStorage.getItem('token') === null || localStorage.getItem('url') === null) {
      window.location.replace("/login");
    }

    const url = localStorage.getItem("url") + "/users";

    axios.get(url, {
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      }
    }).then((response) => {
      setUsers(response.data.users);
    }).catch((error) => {
      setErrorMessage('Error fetching users');
      showPopup();
    });
  }, []);
    
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

    const handleNav = () => {
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

    const handleCreateUserSubmit = (e) => {
        e.preventDefault();
        // allow e.preventDefault() to work
        // Event.preventDefault();
        hidePopup();
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const pword = document.getElementById('pword').value;
        const cnfrmpword = document.getElementById('cnfrmpword').value;
        const teampword = document.getElementById('teampword').value;

        if(pword !== cnfrmpword) {
          setErrorMessage('Passwords do not match');
          showPopup();
          return;
        }

        // Check if username already in list:
        for(let i = 0; i < users.length; i++) {
          if(users[i].username === username) {
            setErrorMessage('Username already exists');
            showPopup();
            return;
          }
        }

        const url = localStorage.getItem("url") + "/register";
        console.log("URL: ", url);

        axios.post(url, {
          username: username,
          email: email,
          password: pword,
          confirm_password: cnfrmpword,
          team_password: teampword
        }).then((response) => {
          if(response.data.status === 'success') {
            setErrorMessage('User created successfully');
            showPopup(true);
            setTimeout(() => {
              window.location.reload();
            }, 1000);
          }
          else {
            setErrorMessage(response.data.msg);
            showPopup();
          }
        }).catch((error) => {
            setErrorMessage(error.data.msg);
            showPopup();
            return;
        });
    }

    const handleCreateUser = () => {
      hidePopup();
      const createFormPage = document.getElementById('createFormPage');
      createFormPage.classList.toggle('top-position');
    }


    return (
       <div>
           <div className="form-page" id="createFormPage">
            <div className="logo-section-light show" id="div5">
              <img
                src={rd03}
                alt="logo"
                className="logo-create-Light"
                id="createLogoLight"
              />
            </div>
            <div className="logo-section-dark hide" id="div6">
              <img
                src={rd04}
                alt="logo"
                className="logo-create-dark"
                id="createLogoDark"
              />
            </div>
            <form className="form">
              <div className="form-scroll">
              <input className="input-create-list" type="text" placeholder="Username" id='username' required="required" />
              <input className="input-create-list" type="text" placeholder="Email" id='email' required="required" />
              <input className="input-create-list" type="password" placeholder="Password" id='pword' required="required" />
              <input className="input-create-list" type="password" placeholder="Confirm Password" id='cnfrmpword'  required="required" />
              <input className="input-create-list" type="password" placeholder="Team Password" id='teampword'  required="required" />
              <input type="submit" onClick={handleCreateUserSubmit} value="Create User" className="sub-list" />
              </div>
            </form>
          </div>
          <div className="toggle-container">
            <input onClick={handleDark} onChange={handleChangeDark} type="checkbox" id="toggle" className="toggle-checkbox" />
            <label for="toggle" className="toggle-label">
              <span className="toggle-inner"><i className="fa-solid fa-sun"></i></span>
              <span className="toggle-switch"><i className="fa-solid fa-moon"></i></span>
            </label>
          </div>
          <div className="logo-light show" id="div3">
            <img src={rd01} alt="LOGO" />
          </div>
          <div className="logo-dark hide" id="div4">
            <img src={rd02} alt="LOGO" />
          </div>
          <div className="users">
            <div className="container">
              <div className="navbar" id="navbar">
                <div className="navbar-logo-light visible" id="div1">
                  <img src={rd01} alt="LOGO" />
                </div>
                <div className="navbar-logo-dark hidden" id="div2">
                  <img src={rd02} alt="LOGO" />
                </div>
                <button onClick={handleNav} id="stretchButton" className="stretch-button">
                  <span className="arrow-icon"></span>
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
              <div className="content" id="content">
                <div className="user">
                  <h2 className="heading" id="mySection">Users List</h2>
                  <button className="create" onClick={handleCreateUser} id="create">Create User</button>
                </div>
                <div className="user-menu">
                  <div className="id user-menu-child lmlc1">
                    ID &nbsp;<i className="fa-solid fa-up-down"></i>
                  </div>
                  <div className="name user-menu-child lmlc2">
                    Name &nbsp;<i className="fa-solid fa-up-down"></i>
                  </div>
                  <div className="email user-menu-child">
                    Email &nbsp;<i className="fa-solid fa-up-down"></i>
                  </div>
                  <div className="type user-menu-child">
                    Type &nbsp;<i className="fa-solid fa-up-down"></i>
                  </div>
                  <div className="last-logon user-menu-child lmlc3">
                    Last Logon &nbsp;<i className="fa-solid fa-up-down"></i>
                  </div>
                  {/* <div className="operations user-menu-child">Operations</div> */}
                </div>
                <div className="user-items">
                  <div className="user-items-scroll">
                    { users.map((user) => (
                    <div className="dummy" key={user.id}>
                      <div className="dummy-child dlc1">{user.id}</div>
                      <div className="dummy-child dlc2">{user.username}</div>
                      <div className="dummy-child dlc2 email-div">{user.email}</div>
                      <div className="dummy-child dlc2">Administrator</div>
                      <div className="dummy-child dlc3">Online</div>
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
