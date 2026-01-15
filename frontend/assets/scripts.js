document.addEventListener("DOMContentLoaded", () => {

    const el = document.querySelector("content");
    const ft = document.querySelector("footer");
    const checkbox = document.querySelector(".lock-checkbox input");
    console.log(checkbox);
    const notification = document.getElementById("lock-notification");

    let notificationTimeout = null;

    const savedOrder = JSON.parse(localStorage.getItem("order"));

    if (savedOrder && el) {
        savedOrder.forEach(id => {
            const item = document.getElementById(id);
            if (item) el.appendChild(item);
        });
    }

    const sortable = new Sortable(el, {
        animation: 150,
        ghostClass: "ghost",
        easing: "cubic-bezier(1, 0, 0, 1)",
        direction: "horizontal",
        disabled: checkbox.checked,

        onSort: () => {
            const ids = [...el.children].map(child => child.id);
            localStorage.setItem("order", JSON.stringify(ids));
        },

        onStart: () => {
            el.style.cursor = "grabbing";
            el.style.backgroundColor = "#edb937";
            ft.style.backgroundColor = "#edb937";
        },

        onEnd: () => {
            el.style.cursor = "default";
            el.style.backgroundColor = "transparent";
            ft.style.backgroundColor = "transparent";
        }
    });

    function showNotification(text) {
        notification.textContent = text;
        notification.classList.add("show");

        clearTimeout(notificationTimeout);
        notificationTimeout = setTimeout(() => {
            notification.classList.remove("show");
        }, 2000);
    }

    function onLockChange(isLocked) {
        sortable.option("disabled", isLocked);

        if (isLocked) {
            showNotification("🔒 Układ kard zablokowany. Kliknij w kłódkę, żeby uporządkować układ kart.");
        } else {
            showNotification("🔓 Możesz teraz zmienić kolejność kart blogów.");
        }
    }

    onLockChange(checkbox.checked);

    checkbox.addEventListener("change", e => {
        onLockChange(e.target.checked);
    });

});