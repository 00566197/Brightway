document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('entryModal');
    const form = document.getElementById('entryForm');

    if (!localStorage.getItem('autoforge_entry_confirmed')) {
        modal.style.display = 'flex';
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        localStorage.setItem('autoforge_entry_confirmed', 'true');
        modal.style.display = 'none';
    });
});