function setActiveNav() {
  const currentPage = window.location.pathname
    .split("/")
    .pop()
    .toLowerCase();

  const items = document.querySelectorAll(".sidebar-item");

  items.forEach(item => {
    const href = item.getAttribute("href").toLowerCase();
    item.classList.toggle("active", href === currentPage);
  });
}

fetch("navbar.html")
  .then(res => res.text())
  .then(html => {
    document.getElementById("navbar").innerHTML = html;
    setActiveNav(); 
  });
