// JavaScript to toggle mobile menu
if (document.getElementById('menu-toggle')) {
    document.getElementById('menu-toggle').addEventListener('click', function () {
        var menu = document.getElementById('mobile-menu');
        menu.classList.toggle('hidden');
    });
}

// JavaScript to handle theme switching and save the preference
const themeSwitcher = document.getElementById('theme-switcher');
const currentTheme = localStorage.getItem('theme') || 'corporate';

if (currentTheme === 'business') {
    document.documentElement.setAttribute('data-theme', 'business');
    themeSwitcher.checked = true;
} else {
    document.documentElement.setAttribute('data-theme', 'corporate');
}

themeSwitcher.addEventListener('change', function () {
    if (this.checked) {
        document.documentElement.setAttribute('data-theme', 'business');
        localStorage.setItem('theme', 'business');
    } else {
        document.documentElement.setAttribute('data-theme', 'corporate');
        localStorage.setItem('theme', 'corporate');
    }
});



// JavaScript to load messages from the server and auto-dismiss them
document.body.addEventListener('htmx:afterRequest', function () {
    fetch("/messages/")
        .then(response => response.text())
        .then(html => {
            document.querySelector('#message-container').innerHTML = html;

            // Find all alert messages and set a timeout to hide them
            const alerts = document.querySelectorAll('#message-container .alert');
            alerts.forEach((alert) => {
                setTimeout(() => {
                    alert.classList.add('opacity-0', 'transition-opacity', 'duration-500');
                    setTimeout(() => {
                        alert.remove();
                    }, 500); // Match this to the duration of the transition
                }, 1000); // Hide after 2 seconds
            });
        });
});
