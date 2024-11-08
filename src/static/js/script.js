// initialize select2 to the id_product field in create_bill.html
// $('#id_product').select2();

// Add this function to handle custom discount visibility
function toggleCustomDiscount(radio) {
    const customDiscountInput = document.getElementById('id_custom_discount');
    
    if (radio.value === '-1') {  // Custom discount selected
        customDiscountInput.hidden = false;
        customDiscountInput.required = true;
        customDiscountInput.focus();
    } else {
        customDiscountInput.hidden = true;
        customDiscountInput.required = false;
        customDiscountInput.value = '';
    }
}

// clear the fields after adding a new product used in create_bill.html
function clearFields() {
    document.getElementById('id_quantity').value = '';
    document.getElementById('id_custom_rate').value = '';
    document.getElementById('id_custom_discount').value = '';
    // Reset radio buttons to "No Discount"
    document.querySelector('input[name="discount_type"][value="0"]').checked = true;
    document.getElementById('id_custom_discount').hidden = true;
    document.getElementById('id_custom_rate').focus();
}

// prevent form submission when pressing enter key in create_bill.html
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');

        inputs.forEach((input, index) => {
            input.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    event.preventDefault();
                    
                    // Find the next visible input
                    let nextIndex = index + 1;
                    let nextInput = inputs[nextIndex];
                    while (nextInput && (nextInput.hidden || nextInput.style.display === 'none')) {
                        nextIndex++;
                        nextInput = inputs[nextIndex];
                    }
                    
                    if (nextInput) {
                        nextInput.focus();
                    } else {
                        form.querySelector('input[type="submit"]').click();
                    }
                }
            });
        });
    });
});

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
