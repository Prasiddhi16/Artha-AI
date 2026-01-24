<<<<<<< HEAD
 function ProfileDialogs() {
=======
/*CSRF helper*/ 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function ProfileDialogs() {
>>>>>>> 5d49889de660bbeec3da84473860add09db5fc2e
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


<<<<<<< HEAD
const csrftoken = document.querySelector('meta[name="csrf-token"]').content;


=======
>>>>>>> 5d49889de660bbeec3da84473860add09db5fc2e
  
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
<<<<<<< HEAD
=======
   
    //profile picture
const input = document.getElementById('profile-image-input');
const uploadBtn = document.getElementById('change-picture');
const circle = document.getElementById('circle');
const initials = document.getElementById('initials');
const img = document.getElementById('profile-circle-img');

// Set initials from data attribute 
if (initials && circle && circle.dataset.initials) {
    initials.textContent = circle.dataset.initials.toUpperCase();
}

if (uploadBtn && input) {
    uploadBtn.addEventListener('click', e => {
        e.preventDefault();
        input.click();
    });

    input.addEventListener('change', () => {
        const file = input.files[0];
        if (!file) return;

        // check if img exists
        if (img) {
            img.src = URL.createObjectURL(file);
            img.style.display = 'block';
            if (initials) initials.style.display = 'none';
        }

        // Upload via AJAX
        const formData = new FormData();
        formData.append('profile_image', file);
        
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfInput) {
            formData.append('csrfmiddlewaretoken', csrfInput.value);
        }

        fetch('/upload-profile-picture/', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                console.log('Profile image updated!');
            } else {
                alert('Upload failed!');
            }
        })
        .catch(error => {
            console.error('Upload error:', error);
            alert('Upload failed!');
        });
    });
}

//email modal
const changeEmailBtn = document.getElementById('change-email-btn');
    const emailModal = document.getElementById('change-email-modal');
    
    if (changeEmailBtn && emailModal) {
        changeEmailBtn.addEventListener('click', () => {
            emailModal.style.display = emailModal.style.display === 'none' ? 'block' : 'none';
        });
    }
//email
   const sendOtpBtn = document.getElementById('send-otp-btn');
    if (sendOtpBtn) {
        console.log('Email OTP button found'); // Debug
        
        sendOtpBtn.addEventListener('click', async () => {
            console.log('Send OTP clicked'); // Debug
            
            const newEmailInput = document.getElementById('new-email');
            if (!newEmailInput) {
                alert("Email input not found");
                return;
            }
            
            const newEmail = newEmailInput.value;
            if (!newEmail) {
                alert("Please enter a new email");
                return;
            }
            
            try {
                const res = await fetch('/request-email-change/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ new_email: newEmail })
                });
                
                const data = await res.json();
                alert(data.message);
                
                if (data.success) {
                    window.location.href = "/verify-email/";
                }
            } catch (error) {
                console.error('Email change error:', error);
                alert('An error occurred while requesting email change');
            }
        });
    } else {
        console.warn('Send OTP button not found');
    }
    //export settings
    document.getElementById('export-settings')?.addEventListener('click', () => {
    window.location.href = '/export-settings/';
    });

    //clear data
    document.getElementById('clear-data')?.addEventListener('click', async () => {
     const confirmation = prompt("Type DELETE to confirm:");
    if (!confirmation) return;
    const res = await fetch('/clear-data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ confirm: confirmation })
    });
    
    const data = await res.json();
    alert(data.message);
    
    if (data.success) {
        window.location.reload();
    }
});
>>>>>>> 5d49889de660bbeec3da84473860add09db5fc2e
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', ProfileDialogs);
