console.log("🔔 Notification JS loaded");

document.addEventListener("DOMContentLoaded", function () {
    // --- DOM elements ---
    const notifContainer = document.getElementById("notif-container");
    const notifContent = document.getElementById("notif-content");
    const notifList = document.getElementById("notif-list");
    const notifCount = document.getElementById("notif-count");
    const openBtn = document.getElementById("openNotifications");

    // Array to store notifications
    let notifications = [];

    // --- Toggle notification overlay ---
    if (openBtn && notifContainer) {
        openBtn.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            notifContainer.style.display =
                notifContainer.style.display === "block" ? "none" : "block";
        });
    }

    // --- Click outside closes overlay ---
    if (notifContainer) {
        notifContainer.addEventListener("click", (e) => {
            if (e.target === notifContainer) {
                notifContainer.style.display = "none";
            }
        });
    }

    // --- Prevent closing when clicking inside box ---
    if (notifContent) {
        notifContent.addEventListener("click", (e) => {
            e.stopPropagation();
        });
    }

    // --- Function to update notification list and badge ---
    function updateNotifications() {
        // Update badge
        if (notifCount) {
            notifCount.textContent = notifications.length;
            notifCount.style.display = notifications.length ? "inline-block" : "none";
        }

        // Update list
        if (notifList) {
            notifList.innerHTML = "";
            notifications.slice().reverse().forEach((notif) => {
                const li = document.createElement("li");
                li.textContent = notif.message;

                // Style based on type
                if (notif.type === "warning") li.style.color = "orange";
                if (notif.type === "error") li.style.color = "red";
                if (notif.type === "success") li.style.color = "green";

                notifList.appendChild(li);
            });
        }
    }

    // --- Demo notification (for testing) ---
    setTimeout(() => {
        notifications.push({ message: "Welcome to Artha AI!", type: "success" });
        updateNotifications();
    }, 2000);

    // --- WebSocket for real-time notifications ---
    function connectWebSocket() {
        const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
        const wsPath = `${wsScheme}://${window.location.host}/ws/notifications/`;
        const socket = new WebSocket(wsPath);

        socket.onopen = function () {
            console.log("✅ WebSocket connected:", wsPath);
        };

        socket.onmessage = function (e) {
            const data = JSON.parse(e.data);
            if (data.message) {
                notifications.push({
                    message: data.message,
                    type: data.type || "info",
                });
                updateNotifications();
            }
        };

        socket.onclose = function () {
            console.log("⚠️ WebSocket closed. Reconnecting in 3s...");
            setTimeout(connectWebSocket, 3000);
        };

        socket.onerror = function (e) {
            console.error("WebSocket error:", e);
            socket.close();
        };
    }

    connectWebSocket();
});