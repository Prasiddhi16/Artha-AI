document.addEventListener("DOMContentLoaded", function () {
    const notifContainer = document.getElementById("notif-container");
    const notifContent = document.getElementById("notif-content");
    const notifList = document.getElementById("notif-list");
    const notifCount = document.getElementById("notif-count");
    const openBtn = document.getElementById("openNotifications");
    const markAllReadBtn = document.getElementById("markAllReadBtn");
    const clearNotifBtn = document.getElementById("clearNotifBtn");

    let notifications = [];

    // ---------- CSRF ----------
    function getCSRFToken() {
        return document
            .querySelector("meta[name='csrf-token']")
            ?.getAttribute("content");
    }

    // ---------- UI ----------
    function updateNotifications() {
        const unreadCount = notifications.filter(n => !n.is_read).length;

        notifCount.textContent = unreadCount;
        notifCount.style.display = unreadCount ? "inline-block" : "none";

        notifList.innerHTML = "";

        notifications.forEach(n => {
            const li = document.createElement("li");
            li.textContent = n.message;

            if (!n.is_read) li.style.fontWeight = "bold";

            if (n.notification_type === "warning") li.style.color = "orange";
            if (n.notification_type === "error") li.style.color = "red";
            if (n.notification_type === "success") li.style.color = "green";
            if (n.notification_type === "info") li.style.color = "blue";

            notifList.appendChild(li);
        });

        // disable buttons when useless
        markAllReadBtn.disabled = unreadCount === 0;
        clearNotifBtn.disabled = notifications.length === 0;
    }

    // ---------- Fetch ----------
    async function fetchNotifications() {
        try {
            const res = await fetch("/api/notifications/");
            if (!res.ok) throw new Error("Fetch failed");
            const data = await res.json();
            notifications = data.notifications || [];
            updateNotifications();
        } catch (err) {
            console.error("Notification fetch error:", err);
        }
    }

    // ---------- Actions ----------
    async function markAllRead() {
        try {
            const res = await fetch("/api/notifications/read/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json",
                },
            });

            if (!res.ok) throw new Error("Mark read failed");

            notifications.forEach(n => n.is_read = true);
            updateNotifications();
        } catch (err) {
            console.error(err);
        }
    }

    async function clearNotifications() {
        try {
            const res = await fetch("/api/notifications/clear/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json",
                },
            });

            if (!res.ok) throw new Error("Clear failed");

            notifications = [];
            updateNotifications();
        } catch (err) {
            console.error(err);
        }
    }

    // ---------- Events ----------
    openBtn?.addEventListener("click", async (e) => {
        e.preventDefault();
        e.stopPropagation();

        const isOpening = notifContainer.style.display !== "block";
        notifContainer.style.display = isOpening ? "block" : "none";

        if (isOpening) await fetchNotifications();
    });

    markAllReadBtn?.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        markAllRead();
    });

    clearNotifBtn?.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        clearNotifications();
    });

    notifContainer?.addEventListener("click", e => {
        if (e.target === notifContainer) notifContainer.style.display = "none";
    });

    notifContent?.addEventListener("click", e => e.stopPropagation());

    // ---------- Polling ----------
    setInterval(fetchNotifications, 15000);
    fetchNotifications();
});
