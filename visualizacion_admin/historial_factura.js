const dropdownToggle = document.querySelector(".usuario");
const dropdownMenu = document.querySelector(".dropdown-usuario");

dropdownToggle.addEventListener("click", () => {
  dropdownMenu.classList.toggle("visible");
});

window.addEventListener("click", function (e) {
  if (!dropdownToggle.contains(e.target) && !dropdownMenu.contains(e.target)) {
    dropdownMenu.classList.remove("visible");
  }
});
