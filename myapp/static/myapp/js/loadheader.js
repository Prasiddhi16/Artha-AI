document.addEventListener("DOMContentLoaded", function () {
    const openuser = document.getElementById("openuser");
    const usercontainer = document.getElementById("user-container");

    // Safety check, if elements don't exist on current page, do nothing
    if (!openuser || !usercontainer) return;

    // Open dropdown when clicking the user button/icon
    openuser.addEventListener("click", function (e) {
        e.stopPropagation(); // Prevent click from immediately closing
        usercontainer.style.display = "block";
    });

    // Close when clicking outside the dropdown
    window.addEventListener("click", function () {
        usercontainer.style.display = "none";
    });

    // Prevent closing when clicking inside the dropdown
    usercontainer.addEventListener("click", function (e) {
        e.stopPropagation();
    });
});