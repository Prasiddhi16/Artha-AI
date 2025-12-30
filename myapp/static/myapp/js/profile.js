       function ProfileDialogs() {
       const overlay=document.querySelector(".overlay");
       const profile=document.querySelector(".profile-button");
       const settings=document.querySelector(".settings-button");
       const logout=document.querySelector(".logout-button");
       const pdialog=document.querySelector("#profile-dialog");
       const sdialog=document.querySelector("#settings-dialog");
       
    // Safety check, if elements don't exist on current page, do nothing
       if (!overlay || !profile || !settings) return;


       //open dialogs
        profile.onclick = (e) => {
            e.stopPropagation();
            pdialog.style.display="block";
            overlay.style.display="flex";
            sdialog.style.display="none";
       };

        settings.onclick = (e) => {
            e.stopPropagation();
            sdialog.style.display="block";
            overlay.style.display="flex";
            pdialog.style.display="none";
        };

        //close dialogs
        overlay.onclick = (e) => {
            if(e.target===overlay){
            overlay.style.display="none";
            }
        };

        // prevents closing when clicking inside the dialog
        pdialog.onclick = (e) => {  e.stopPropagation()};
        sdialog.onclick = (e) => {  e.stopPropagation()};
      

        //switching tabs
        const profiletab=document.getElementById("profile-tab");
        const notiftab =document.getElementById("notification-tab");
        const securitytab=document.getElementById("security-tab");
        const psection=document.querySelectorAll(".psection");
        const ptab=document.querySelectorAll(".tab");
       

        function switchTab(tabname){
            ptab.forEach(sec=>
            {sec.classList.remove("active")});
            document.getElementById(tabname).classList.add("active"); 
        }

        function switchSection(sectionname){
            psection.forEach(sec=>
            {sec.classList.remove("active")});
            document.getElementById(sectionname).classList.add("active"); 
        } 

        if (profiletab) {
        profiletab.onclick = () => {
        switchTab("profile-tab");
        switchSection("profile-section");
        }};

        if (notiftab) {
        notiftab.onclick = () => {
        switchTab("notification-tab");
        switchSection("notification-section");
        }};

        if (securitytab) {
        securitytab.onclick = () => {
        switchTab("security-tab");
        switchSection("security-section");
        }};
    }
