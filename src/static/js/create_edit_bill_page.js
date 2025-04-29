
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

    // Listen for HTMX beforeOnLoad event to update the errors if any
    document.addEventListener('htmx:beforeOnLoad', function (event) {
        if (event.detail.xhr.status === 400) {
            // Display error message in the appropriate div
            document.querySelector('#bill_item_form_errors').innerHTML = event.detail.xhr.responseText;
        }
    });
});