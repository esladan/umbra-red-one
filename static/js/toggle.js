
function toggleanimate() {
    let toggleAnimate = document.querySelector(".ham-nav");
    let toggle = document.querySelector(".dropbtn");
    let backdrop = document.querySelector(".back-drop");
    if(toggleAnimate.className === "ham-nav" || toggle.className === "dropbtn"){
        toggleAnimate.className += " active";
        toggle.className += " open";
        backdrop.style.display = "block";
    }
    else{
        toggleAnimate.className = "ham-nav";
        toggle.className = "dropbtn";
        backdrop.style.display = "none";
    }
}

let navAnimateToggle = document.querySelector(".ham-nav");
navAnimateToggle.addEventListener("click", toggleanimate);

// Dashboard daemon
function formToggler(){
    let formToggle = document.querySelector(".form-toggle");
    let formBox = document.querySelector(".formbox");
 
    let backdrop = document.querySelector(".back-drop");
    if(formToggle.className === "form-toggle"){
        formToggle.className += " on";
        formBox.className += " open";
        backdrop.style.display = "block";
    }else {
        formToggle.className = "form-toggle";
        formBox.className = "formbox";
         backdrop.style.display = "none";
    }
}

let formToggle = document.querySelector(".form-toggle");
formToggle.addEventListener("click", formToggler);


// Toppings daemon
function openToppings(){
    let toppings = document.querySelector(".toppings");
    if(toppings.className === "toppings"){
        toppings.className += " open";
    }
    else {
        toppings.className = "toppings";
    }
}

let toppingsVar = document.querySelector(".toppings");
toppingsVar.addEventListener("click", openTopping);