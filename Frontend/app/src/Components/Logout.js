import axios from "axios";


export default function Logout() {

    console.log("Here");

    const logout = async() => {
        try {
            const url = localStorage.getItem('url');
            if(url === null) {
                window.location.href = "/login";
            }
            axios.get(url + "/logout", {
                headers: {
                    'Content-Type' : 'application/json',
                    'Accept' : 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                }
            }).then((response) => {
                localStorage.removeItem("token");
                localStorage.removeItem("url");
                window.location.href = "/login";
            }).catch((error) => {
                console.log("Error:");
                console.log(error);
            }
            );
        }
        catch (error) {
            console.log("Error:");
            console.log(error);
        }
    }
    logout();
}