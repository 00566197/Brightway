function openSideMenu(){
    document.getElementById('side-menu').style.width ='250px';
}

function closeSideMenu(){
    document.getElementById('side-menu').style.width ='0';
}
document.addEventListener("DOMContentLoaded", function () { 
    const dropdownBtns = document.querySelectorAll(".dropdown-btn");
    dropdownBtns.forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault(); 
            this.closest(".dropdown").classList.toggle("active");
        });
    });
});
 