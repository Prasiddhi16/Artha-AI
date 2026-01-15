document.addEventListener("DOMContentLoaded", () => {
  const openuser = document.getElementById("openuser");
  const userContainer = document.getElementById("user-container");
  const userContent = document.getElementById("user-content");

   // Safety check, if elements don't exist on current page, do nothing
    if (!openuser || !userContainer) return;

    // Open dropdown when clicking the user button/icon
    openuser.addEventListener("click", (e) => {
    e.preventDefault();   //prevent href="#"
    e.stopPropagation();  //ICON → DIALOG → OVERLAY → BODY → WINDOW.Prevents the click from going above overlay

    fetch("/profile/")
      .then(res => res.text())
      .then(html => {
        userContent.innerHTML = html;
        userContainer.style.display = "block";

    // profile.js logic's safe check and execution
                if (typeof ProfileDialogs === "function") {
                    ProfileDialogs();
                }
            });
  });

  // Close when clicking outside the dropdown
  userContainer.addEventListener("click", (e) => {
    if(e.target === userContainer){
    userContainer.style.display = "none";}
  });
  
    // Prevents closing when clicking inside the dropdown
  userContent.addEventListener("click", (e)=>{
    e.stopPropagation();
 });
    
});
