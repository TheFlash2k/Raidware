import '../styles/Popup.css';

const hidePopup = () => {
    const err_popup = document.getElementById('err-popup');
    if(err_popup === null) { return; }
    // background-color: hsla(0, 100%, 50%, 0.603);
    err_popup.style.backgroundColor = "hsla(0, 100%, 50%, 0.603)";
    err_popup.style.opacity = "0";
    err_popup.style.visibility = "hidden";
}

// Create showPopup function that has named parameters for the title and message
const showPopup = (success = false) => {
    const err_popup = document.getElementById('err-popup');
    if(err_popup === null) { return; }

    if(success) {
        err_popup.style.backgroundColor = "hsla(108, 97%, 46%, 0.603)";
    }

    err_popup.style.display = "block";
    err_popup.style.opacity = "1";
    err_popup.style.visibility = "visible";

}

export { showPopup, hidePopup };