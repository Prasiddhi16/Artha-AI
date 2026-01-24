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

            // Apply type-specific class
            if (n.notification_type === "warning") li.classList.add("notif-warning");
            if (n.notification_type === "error") li.classList.add("notif-error");
            if (n.notification_type === "success") li.classList.add("notif-success");
            if (n.notification_type === "info") li.classList.add("notif-info");

            // Message span
            const msgSpan = document.createElement("span");
            msgSpan.textContent = n.message;
            if (!n.is_read) msgSpan.style.fontWeight = "bold";

            // Relative time span
            const dateSpan = document.createElement("span");
            dateSpan.classList.add("notif-date");
            dateSpan.textContent = timeAgo(n.client_created_at);

            li.appendChild(msgSpan);
            li.appendChild(dateSpan);
            notifList.appendChild(li);
        });

        markAllReadBtn.disabled = unreadCount === 0;
        clearNotifBtn.disabled = notifications.length === 0;
    }

    // ---------- Fetch ----------
    async function fetchNotifications() {
        try {
            const res = await fetch("/api/notifications/");
            if (!res.ok) throw new Error("Fetch failed");
            const data = await res.json();

            notifications = (data.notifications || []).map(n => ({
                ...n,
                // Parse server timestamp into a Date object
                client_created_at: new Date(n.created_at)
            }));

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

    function timeAgo(date) {
        // Compare absolute timestamps to avoid timezone offset issues
        const seconds = Math.floor((Date.now() - date.getTime()) / 1000);

        let interval = Math.floor(seconds / 31536000);
        if (interval >= 1) return interval + " year" + (interval > 1 ? "s" : "") + " ago";

        interval = Math.floor(seconds / 2592000);
        if (interval >= 1) return interval + " month" + (interval > 1 ? "s" : "") + " ago";

        interval = Math.floor(seconds / 86400);
        if (interval >= 1) return interval + " day" + (interval > 1 ? "s" : "") + " ago";

        interval = Math.floor(seconds / 3600);
        if (interval >= 1) return interval + " hour" + (interval > 1 ? "s" : "") + " ago";

        interval = Math.floor(seconds / 60);
        if (interval >= 1) return interval + " minute" + (interval > 1 ? "s" : "") + " ago";

        return "just now";
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