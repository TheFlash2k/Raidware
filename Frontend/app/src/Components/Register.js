import { useEffect, useState } from 'react';
import logo from './resources/rd-01.png';
import logo_inverted from './resources/rd-01 inverted.png';
import './styles/Register.css'
import axios from "axios";
import { showPopup, hidePopup } from "./utils/Popup";
import './styles/Popup.css'

export default function Register() {

    const [errorMessage, setErrorMessage] = useState("");

    useEffect(() => {
        hidePopup();
    }, []);

    const handleDark = () => {
        const div1 = document.getElementById("div1");
        const div2 = document.getElementById("div2");
        if (div1.classList.contains("visible")) {
            div1.classList.add("hidden");
            div2.classList.add("visible");
            div1.classList.remove("visible");
            div2.classList.remove("hidden");
          } else {
            div1.classList.add("visible");
            div2.classList.add("hidden");
            div2.classList.remove("visible");
            div1.classList.remove("hidden");
          }
    }

    const handleChangeDark = () => {
        const body = document.body;
        body.classList.toggle("dark-mode");
    }

    const handleRegister = (e) => {
        hidePopup();
        e.preventDefault();
        // Get the form fields:
        const email = document.getElementById("login-email").value;
        const username = document.getElementById("login-user").value;
        const password = document.getElementById("login-password").value;
        const url = document.getElementById("login-url").value;
        const confirm_p = document.getElementById("login-confirmp").value;
        const team = document.getElementById("login-teamp").value;

        if (
            username === "" || password === "" || team === "" || url === "" || email === "" || confirm_p === ""
            || username === null || password === null || team === null || url === null || email === null || confirm_p === null
        ) {
            setErrorMessage("Please fill out all fields.");
            showPopup();
            return;
        }
        const api_url = "http://" + url + "/v1";
        // Check if the server is up:
        axios.get(api_url + "/version").then((response) => {
            if(response.status === 200) {
                console.log("Server is up, continuing with login");
                localStorage.setItem("url", api_url);
            }
        }).catch((error) => {
            setErrorMessage("Unable to communicate with the teamserver.\nPlese check the URL and try again.");
            showPopup();
            return;
        });

        const data = {
            username: username,
            email: email,
            password: password,
            confirm_password: confirm_p,
            team_password : team
        }

        console.log("Data: ", data)

        axios.post(api_url + "/register", data).then((response) => {
            // sleep for 2 seconds to allow the user to see the success message
            setErrorMessage("Successfully registered! Redirecting to login page...");
            showPopup(true);
            setTimeout(() => {
                window.location.href = "/login";
            }, 1000);
        }
        ).catch((error) => {
            setErrorMessage(error.response.data.msg);
            showPopup();
            return;
        }
        );
        
    }

    return (
        <div>
            <div class="toggle-container">
                <input onClick={handleDark} onChange={handleChangeDark} type="checkbox" id="toggle" class="toggle-checkbox" />
                <label for="toggle" class="toggle-label">
                    <span class="toggle-inner"><i class="fa-solid fa-sun"></i></span>
                    <span class="toggle-switch"><i class="fa-solid fa-moon"></i></span>
                </label>
            </div>
            
            <div class="mainLogin">
            <form class="login-section">
                <div class="error-popup" id="err-popup">
                    <button onClick={hidePopup}>
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div>{errorMessage}</div>
                </div>
                <div class="logo-sec" id="login-logo-sec">
                <img src={logo} alt="logo" class="logo visible" id="div1" />
                <img src={logo_inverted} alt="logo" class="logo hidden" id="div2" />
                </div>
                <div class="url-sec">
                    <input class="input-url-disabled" type="url" name="" id="login-url-dis" placeholder="https://" required="required" disabled="disabled" />
                    <input class="input-url" type="url" name="" id="login-url" placeholder="Teamserver URL" required="required" />
                </div>
                <input class="input" type="email" id="login-email" placeholder="Email" required="required" />
                <input class="input" type="text" name="" id="login-user" placeholder="Username" required="required" />
                <input class="input" type="password" name="" id="login-password" placeholder="Password" required="required" />
                <input class="input" type="password" name="" id="login-confirmp" placeholder="Confirm Password" required="required" />
                <input class="input" type="password" name="" id="login-teamp" placeholder="Team Password" required="required" />    
                <p><b>&nbsp;&nbsp;&nbsp;Already a user?</b> <a href="/login">Login</a></p>
                <input onClick={handleRegister} type="submit" value="Register" class="button" id="login-submit" />
            </form>
            </div>
        </div>
    );
}