document.addEventListener("DOMContentLoaded", (ev) => {

    const el = document.querySelector('content');
    const ft = document.querySelector('footer');


    // Pobierz zapisany porządek
    const savedOrder = JSON.parse(localStorage.getItem('order'));

    if (savedOrder) {
        savedOrder.forEach(id => {
            const item = document.getElementById(id);
            if (item) el.appendChild(item);
        });
    }

    // Inicjalizacja sortowania
    new Sortable(el, {
        animation: 150,
        ghostClass: "ghost",
        easing: "cubic-bezier(1, 0, 0, 1)",
        direction: 'horizontal',
        onSort: () => {
            const ids = [...el.children].map(child => child.id);
            localStorage.setItem('order', JSON.stringify(ids));
        },
        onStart: (evt) => {
            el.style.cursor = "grabbing";
            el.style.backgroundColor = "#edb937";
            ft.style.backgroundColor = "#edb937";

        },
        onEnd: (evt) => {   
            el.style.backgroundColor = "transparent";
            ft.style.backgroundColor = "transparent";
        }
    });

});
