# Billing System

A modern billing system built with Django, Tailwind CSS, and HTMX. The system features a responsive design with light/dark theme support and real-time updates.

## Live Demo
The system is live at: http://midknightdev.pythonanywhere.com/
- Username: admin
- Password: 123

## Customization
You can customize the business name throughout the application by setting the `BUSINESS_NAME` environment variable in your `.env` file:

```bash
# Add to your .env file
BUSINESS_NAME="Your Business Name"
```

This will automatically update the business name across:
- Admin interface
- Navigation bar
- Page titles
- Printed bills
- All other relevant places in the application

If `BUSINESS_NAME` is not set, it defaults to "Billing System".

## Features

- 🛍️ Product management
  - Add, edit products through admin panel
  - Set default rates for products
  - Product search with Select2
  - **Enhanced barcode scanning** for quick product selection:
    - Scan barcodes from create/edit bill page
    - **NEW: Quick product lookup from dashboard**
    - **NEW: Product details modal for scanned items**
- 📊 Sales dashboard with period-wise summaries
  - 7 days sales summary
  - Monthly sales summary
  - 3 months sales summary
  - Filter bills by date, salesperson, and search terms
- 🧾 Bill management
  - Create new bills
  - Add multiple items with custom rates
  - Flexible discount options:
    - Pre-defined discounts (40%, 50%)
    - Custom percentage discount
    - Per-item discount application
  - Print bills in a clean format
  - Edit existing bills
  - Delete bills (with proper permissions)
- 👥 Multi-user support
  - Admin/Owner access to all bills
  - Salesperson can create and manage their own bills
  - Role-based permissions
- 🌓 Light/Dark theme support
- 📱 Responsive design
- ⚡ Real-time updates using HTMX
- 🔐 User authentication and authorization
- 📷 **Enhanced barcode scanning capabilities**:
  - Product selection during bill creation
  - **NEW: Product information lookup from dashboard**
  - Mobile-friendly camera interface
  - Support for multiple barcode formats

## Tech Stack

- **Backend**: Django 4.2
- **Frontend**: 
  - Tailwind CSS 3.4
  - DaisyUI 4.12
  - HTMX 1.18
  - Web Barcode Detector API

- **Database**: SQLite (default Django DB)

## Prerequisites

- Python 3.x
- Node.js and npm
- Git
- Modern browser that supports BarcodeDetector API

## Installation

1. Clone the repository
```bash
git clone https://github.com/jethliya-balaji/Billing-System.git
cd Billing-System
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies
```bash
pip install -r requirements.txt
```

4. Install Node.js dependencies
```bash
npm install
```

5. Create .env file in the root directory
```bash
# Create .env file
touch .env  # On Windows: type nul > .env

# Add the following configuration to .env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=TRUE
ALLOWED_HOSTS=localhost 127.0.0.1
BUSINESS_NAME="Your Business Name"  # Optional: defaults to "Billing System"
```

Note: You can generate a secure secret key using Python:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

6. Run database migrations
```bash
python manage.py migrate
```

7. Create a superuser
```bash
python manage.py createsuperuser
```

## Development

1. Start the Django development server
```bash
python manage.py runserver
```

2. Watch for Tailwind CSS changes
```bash
npm run dev
```

## Project Structure

```
Billing-System/
├── src/
│   ├── billing/                    # Main Django app
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── delete_empty_bills.py
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   └── 0001_initial.py
│   │   ├── __init__.py
│   │   ├── admin.py               # Admin interface configuration
│   │   ├── apps.py               # App configuration
│   │   ├── filters.py            # Bill filtering logic
│   │   ├── forms.py              # Form definitions
│   │   ├── models.py             # Database models
│   │   ├── tests.py             # Test cases
│   │   ├── urls.py              # URL routing
│   │   └── views.py             # View logic
│   ├── core/                     # Project settings
│   │   ├── __init__.py
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # Main URL configuration
│   │   └── wsgi.py              # WSGI configuration
│   ├── static/
│   │   ├── css/
│   │   │   └── tailwind-output.css   # Compiled Tailwind CSS
│   │   ├── js/
│   │   │   ├── script.js        # General JavaScript
│   │   │   ├── barcode-scanner.js  # Barcode scanning functionality 
│   │   │   └── create_edit_bill_page.js  # Bill page specific logic
│   │   ├── htmx.min.js          # HTMX library
│   │   └── src/
│   │       └── tailwind-input.css    # Tailwind source
│   └── templates/
│       ├── 403.html             # Permission denied page
│       ├── 404.html             # Not found page
│       └── billing/
│           ├── partials/
│           │   ├── create_edit_bill_item.html
│           │   ├── dashboard_bill.html
│           │   ├── messages.html
│           │   └── navbar.html
│           ├── base.html         # Base template
│           ├── create_edit_bill.html
│           ├── dashboard.html
│           ├── login.html
│           ├── print_bill.html
│           └── view_bill.html
├── .gitignore
├── manage.py                     # Django management script
├── package.json                  # Node.js dependencies
├── requirements.txt              # Python dependencies
└── tailwind.config.js           # Tailwind configuration
```

## Theme Customization

The project uses DaisyUI themes with two default options:
- Corporate (Light theme)
- Business (Dark theme)

Theme preferences are automatically saved to localStorage and persists across sessions.

## Features in Detail

### Product Management
- Add and edit products through Django admin interface
- Set default rates for products
- Products appear in Select2 dropdown during bill creation
- **Enhanced barcode scanning** using device camera for quick selection and lookup
- **Auto-barcode generation** for new products
- **Inventory tracking** with stock management

### Barcode Scanning
- Uses Web BarcodeDetector API for real-time barcode scanning
- Compatible with various barcode formats including Code 128, EAN-13, UPC-A, and QR codes
- **Two scanning modes**:
  - Product selection during bill creation
  - **NEW: Product information lookup from dashboard**
- Camera access with mobile-friendly interface
- Optimized video resolution settings for better scanning performance
- Improved callback pattern for flexible implementation

### Bill Management
- Create new bills with customer details
- Add multiple items with option for custom rates
- Flexible discount options:
  - Pre-defined discounts (40%, 50%)
  - Custom percentage discount
  - Per-item discount application
- Print bills in a clean, professional format
- Edit existing bills (own bills for salesperson, all bills for admin)
- Delete bills with proper permissions
- Automatic bill number generation with date prefix

### Dashboard Features
- View comprehensive sales summaries
- **NEW: Quick product lookup via barcode scanner**
- **NEW: Product details modal for displaying scanned product information**
- Filter bills by:
  - Date
  - Salesperson (admin only)
  - Search terms (customer name, bill number)
- Quick access to recent bills
- Pagination with "Load More" functionality
- Different views for admin and salesperson

### User Management
- Admin/Owner can:
  - View all bills
  - Filter by salesperson
  - Access admin panel
  - Manage products
- Salesperson can:
  - Create new bills
  - View their own bills
  - Edit their own bills
  - Print bills

### Code Organization
- **Improved JavaScript organization**:
  - Core UI functionality in script.js
  - Billing page logic in dedicated create_edit_bill_page.js
  - Barcode scanning functionality in barcode-scanner.js
- Reduced dependencies with optimized script loading
- Better template structure with proper script blocks

## Browser Compatibility

The barcode scanning feature requires a browser that supports the BarcodeDetector API

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License

## Acknowledgments

- [DaisyUI](https://daisyui.com/) for the UI components
- [HTMX](https://htmx.org/) for dynamic interactions
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Select2](https://select2.org/) for enhanced select inputs
- [Django](https://www.djangoproject.com/) for the web framework
- [Web BarcodeDetector API](https://developer.mozilla.org/en-US/docs/Web/API/BarcodeDetector) for barcode scanning capabilities

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/jethliya-balaji/Billing-System/issues).