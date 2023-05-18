import axios from "axios";
import rd01 from '../resources/rd-01 1.png';
import rd02 from '../resources/rd-01 inverted 1.png';


const validateUrl = (_url = null) => {

    if(_url !== null) {
        axios.get(_url + "/version").then((response) => {
            if(response.status === 200) {
                return true;
            }
        }).catch((error) => {
            return false;
        });
    }

    const url = localStorage.getItem('url');
    if(url === null) {
        return false;
    }
    axios.get(url + "/version").then((response) => {
        if(response.status === 200) {
            return true;
        }
    }).catch((error) => {
        return false;
    });
}
const validateToken = () => {

    let url = localStorage.getItem('url');
    let token = localStorage.getItem('token');

    if(url === null) {
        console.log("URL is null");
        return false;
    }
    
    console.log("URL: " + url);
    console.log("Token: " + token);

    if(token !== null && url !== null) {

        const data = {
            token: token
        }
        axios.get(url + "/version", data).then((response) => {
            try {
                if(response.status === 200) {
                    return true;
                }
                else {
                    localStorage.removeItem("token");
                }
            }
            catch(err) {
                localStorage.removeItem("token");
            }
        }).catch((error) => {
            console.log("Error: " + error);
        });
    }
    return false;
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

const Navbar = () => {
    return (
        <div>
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
                    <a href="/listeners"><i class="fa-solid fa-headphones"></i> &nbsp; &nbsp;Listeners</a>
                    <a href="/sessions"><i class="fa-solid fa-briefcase"></i> &nbsp; &nbsp; Session</a>
                    <a href="/agents"><i class="fa-solid fa-users"></i> &nbsp; &nbsp; Agents</a>
                    <a href="/loot"><i class="fa-solid fa-coins"></i> &nbsp; &nbsp; Loot</a>
                    <a href="/users"><i class="fa-solid fa-user"></i> &nbsp; &nbsp; Users</a>
                    <a href="/settings"><i class="fa-solid fa-gear"></i> &nbsp; &nbsp; Settings</a>
                    <a href="/logout" className="logout"><i className="fa-solid fa-right-from-bracket"></i> &nbsp; &nbsp; Log-out</a>
                </div>
            </div>
        </div>
    );
}

export default validateUrl;
export { validateToken, Navbar };