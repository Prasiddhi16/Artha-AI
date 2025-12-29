 const overlay=document.querySelector(".overlay");
       const profile=document.querySelector(".profile-button");
       const settings=document.querySelector(".settings-button");
       const logout=document.querySelector(".logout-button");
       const pdialog=document.querySelector("#profile-dialog");
       const sdialog=document.querySelector("#settings-dialog");
       
       profile.addEventListener("click",()=>{
            pdialog.style.display="block";
            overlay.style.display="flex";
            sdialog.style.display="none";
       });
       window.addEventListener("click", (e) => {
        if (e.target === overlay) {
        overlay.style.display = "none";
        }});
        settings.addEventListener("click",()=>{
            sdialog.style.display="block";
            overlay.style.display="flex";
            pdialog.style.display="none";
        });
        window.addEventListener("click",(e)=>{
            if(e.target===overlay){
            sdialog.style.display="none";
            }
        });

        const profiletab=document.getElementById("profile-tab");
        const notiftab=document.getElementById("notification-tab");
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
        profiletab.addEventListener("click",()=>{
        switchTab("profile-tab");
        switchSection("profile-section");
        });
        notiftab.addEventListener("click",()=>{
        switchTab("notification-tab");
        switchSection("notification-section");
        });
        securitytab.addEventListener("click",()=>{
        switchTab("security-tab");
        switchSection("security-section");
        });
