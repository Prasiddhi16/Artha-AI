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
            pdialog.style.display = "none";
            sdialog.style.display = "none";
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


const csrftoken = document.querySelector('meta[name="csrf-token"]').content;


  
  document.getElementById("save-profile")?.addEventListener("click", async () => {
    const phoneInput = document.getElementById("phone");
    if (!phoneInput) {
        console.error("Phone input not found");
        return;
    }

    const res = await fetch("/profile/update/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      },
      body: JSON.stringify({
        name: document.getElementById("name").value,
        email:document.getElementById("email").value,
        phone:document.getElementById("phone").value
      })
    });

    const data = await res.json();
    if (data.success) {
        alert(data.message);
        // Update display
        document.querySelector('.nameDisplay').textContent = document.getElementById("name").value;
        document.querySelector('.emailDisplay').textContent = document.getElementById("email").value;
    } else {
        alert(data.message);
    }
  });

  
  document.getElementById("save-notifications")?.addEventListener("click", async () => {
    //get checkbox value
    const getCheckboxValue = (id) => {
            const elem = document.getElementById(id);
            if (!elem) {
                console.warn(`Checkbox ${id} not found`);
                return false;
            }
            return elem.checked;
        };
    try{
    const res = await fetch("/profile/notifications/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      },
      body: JSON.stringify({
            email_notifications: getCheckboxValue('email-notif'),
            push_notifications: getCheckboxValue('push-notif'),
            monthly_reports: getCheckboxValue('monthly-report'),
            budget_alerts: getCheckboxValue('budget-alert'),
            goal_reminders: getCheckboxValue('goal-reminder')
      })
    });


    const data = await res.json();
    alert(data.message);

    if (!data.success) {
            console.error("Failed to save notifications:",data);
            }
    } 
    catch (error) {
        console.error("Error saving notifications:", error);
        alert("An error occurred while saving notification preferences");
    }
  });

  /* ---------------- PASSWORD ---------------- */
  document.getElementById("save-password")?.addEventListener("click", async () => {
    const res = await fetch("/profile/password/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      },
      body: JSON.stringify({
        current_password: document.getElementById('current-password').value,
        new_password: document.getElementById('new-password').value,
        confirm_password: document.getElementById('confirm-password').value
      })
    });

    const data = await res.json();
    alert(data.message);
  });



// Two-factor authentication toggle
const authToggle = document.getElementById('authentication');
    if (authToggle) {
        authToggle.onchange = async (e) => { // Using .onchange is safer here
            const data = { enabled: e.target.checked };
    try {
        const response = await fetch('/profile/two-factor/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        alert(result.message);
        if (!result.success) {
                    // Revert on error
                    e.target.checked = !e.target.checked;
                    console.error("Two-factor toggle failed:", result);
                }
    } catch (error) {
        alert('An error occurred. Please try again.');
        e.target.checked = !e.target.checked;
    }
}
};


//privacy
const savePrivacyBtn = document.getElementById('save-privacy');
    if (savePrivacyBtn) {
        savePrivacyBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            
            // Safety check for checkboxes to prevent "null" errors
            const getChecked = (id) => {
                const elem = document.getElementById(id);
                if (!elem) {
                    console.warn(`Privacy checkbox ${id} not found`);
                    return false;
                }
                return elem.checked;
            };

            try {
                const response = await fetch('/profile/privacy/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                analytics_tracking: getChecked('analytics-track'),
                crash_reporting: getChecked('crash-reporting'),
                usage_data: getChecked('usage-data'),
                spending_insights: getChecked('spending-insights')
            })
                });
                const result = await response.json();
                alert(result.message);
            } catch (error) {
                alert('Error saving privacy settings.');
            }
        });
    }

    // Delete Account 
    const deleteBtn = document.getElementById('delete_account');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            if (!confirm('Are you sure? This cannot be undone.')) return;

            try {
                const response = await fetch('/profile/delete/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    }
                });
                const result = await response.json();
                if (result.success) {
                    window.location.href = result.redirect;
                } else {
                    alert(result.message);
                }
            } catch (error) {
                alert('Error deleting account.');
            }
        });
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', ProfileDialogs);
