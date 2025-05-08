// Barcode Scanner Functionality
let videoElement = null;
let stream = null;
let barcodeDetector = null;
let onBarcodeDetectedCallback = null;

function openBarcodeScanner(callback) {
    // Store the callback function
    onBarcodeDetectedCallback = callback;

    // Prevent multiple camera instances
    if (videoElement) {
        closeBarcodeScanner();
        return;
    }

    // Check for Barcode Detector API support
    if (!('BarcodeDetector' in window)) {
        alert('Barcode detection is not supported in this browser.');
        return;
    }

    // Initialize barcode detector with supported formats
    barcodeDetector = new BarcodeDetector({
        formats: [
            'code_128',
            'code_39',
            'ean_13',
            'ean_8',
            'qr_code',
            'upc_a',
            'upc_e'
        ]
    });

    // Create overlay for camera preview
    const overlay = document.createElement('div');
    overlay.id = 'camera-overlay';
    overlay.classList.add(
        'fixed', 'inset-0', 'z-50', 'bg-black', 'bg-opacity-75',
        'flex', 'items-center', 'justify-center', 'flex-col'
    );

    videoElement = document.createElement("video");
    videoElement.classList.add('max-w-full', 'max-h-full', 'rounded-lg');
    videoElement.setAttribute("autoplay", "");
    videoElement.setAttribute("playsinline", "");

    const statusText = document.createElement('div');
    statusText.id = 'scan-status';
    statusText.classList.add('text-white', 'mt-4', 'text-lg');
    statusText.textContent = 'Scanning...';

    const closeButton = document.createElement('button');
    closeButton.textContent = 'Close Camera';
    closeButton.classList.add(
        'mt-4', 'bg-red-500', 'text-white', 'px-4', 'py-2', 'rounded'
    );
    closeButton.addEventListener('click', closeBarcodeScanner);

    overlay.appendChild(videoElement);
    overlay.appendChild(statusText);
    overlay.appendChild(closeButton);
    document.body.appendChild(overlay);

    // Request camera access
    navigator.mediaDevices.getUserMedia({
        video: {
            facingMode: "environment",
            width: { ideal: 250 },
            height: { ideal: 380 }
        }
    })
    .then(mediaStream => {
        stream = mediaStream;
        videoElement.srcObject = mediaStream;

        // Start barcode scanning
        videoElement.onloadedmetadata = () => {
            videoElement.play();
            requestAnimationFrame(scanBarcode);
        };
    })
    .catch(error => {
        console.error("Camera access error:", error);
        alert('Could not access camera. Please check permissions.');
        closeBarcodeScanner();
    });

    async function scanBarcode() {
        if (!videoElement || !barcodeDetector) return;

        try {
            const barcodes = await barcodeDetector.detect(videoElement);
            
            if (barcodes.length > 0) {
                const barcode = barcodes[0].rawValue;
                const statusText = document.getElementById('scan-status');
                statusText.textContent = `Barcode detected: ${barcode}`;
                
                // Call the callback function with the detected barcode
                if (onBarcodeDetectedCallback) {
                    onBarcodeDetectedCallback(barcode);
                }
                
                setTimeout(() => {
                    closeBarcodeScanner();
                }, 500);
            } else {
                requestAnimationFrame(scanBarcode);
            }
        } catch (error) {
            console.error("Barcode detection failed:", error);
            requestAnimationFrame(scanBarcode);
        }
    }
}

function closeBarcodeScanner() {
    // Stop camera stream
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }

    // Remove video element and overlay
    const overlay = document.getElementById('camera-overlay');
    if (overlay) {
        overlay.remove();
    }

    videoElement = null;
    barcodeDetector = null;
    onBarcodeDetectedCallback = null;
}

// Select product by barcode on create/edit bill page
function selectProductByBarcode(barcode) {
    fetch(`/api/product-by-barcode/${barcode}/`)
        .then(response => response.json())
        .then(data => {
            if (data.product_id) {                
                // Select the product in the dropdown
                const productSelect = document.getElementById('id_product');
                productSelect.value = data.product_id;
                
                // Trigger change event to update any dependent fields
                productSelect.dispatchEvent(new Event('change'));
            } else {
                alert('Product not found for this barcode');
            }
        })
        .catch(error => {
            console.error('Error fetching product:', error);
            alert('Error finding product. Please try again or select manually.');
        });
}

// Show product details in modal when barcode is scanned on dashboard
function showProductDetailsFromBarcode(barcode) {
    fetch(`/api/product-by-barcode/${barcode}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Product not found');
            }
            return response.json();
        })
        .then(data => {
            // Populate and show modal
            const contentDiv = document.getElementById('product-details-content');
            
            // Check if user is superuser from the data attribute
            const isSuperuser = document.body.getAttribute('data-is-superuser') === 'true';
            
            contentDiv.innerHTML = `
                <div class="grid grid-cols-2 gap-2 text-lg">
                    <div class="font-bold">Name:</div>
                    <div>${data.name}</div>
                    <div class="font-bold">Rate:</div>
                    <div>${data.default_rate}</div>
                    ${isSuperuser ? `
                        <div class="font-bold">Purchase Rate:</div>
                        <div>${data.purchase_rate}</div>
                    ` : ''}
                    <div class="font-bold">Stock:</div>
                    <div>${data.stock}</div>
                    <div class="font-bold">Barcode:</div>
                    <div>${data.barcode}</div>
                </div>
            `;
            
            // Show modal using DaisyUI's modal system
            const modal = document.getElementById('product-details-modal');
            modal.classList.add('modal-open');
        })
        .catch(error => {
            alert('Product not found for this barcode or error occurred.');
            console.error('Error:', error);
        });
}

// Close product details modal on dashboard
function closeProductModal() {
    const modal = document.getElementById('product-details-modal');
    modal.classList.remove('modal-open');
}