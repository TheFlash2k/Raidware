export default function Darkmode() {

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
        body.classList.toggle("dark-mode");
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
        </div>
    );
}