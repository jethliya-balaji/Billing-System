from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Login & Logout
    path('login/', auth_views.LoginView.as_view(template_name='billing/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Create Bill
    path('bill/create/', views.create_bill, name='create_bill'),

    # Add Item - htmx
    path('bill/add-item/<str:bill_id>/', views.add_item, name='add_item'),

    # Delete Item
    path('bill/delete-item/<int:item_id>/', views.delete_item, name='delete_item'),

    # View Bill
    path('bill/<str:bill_id>/', views.view_bill, name='view_bill'),

    # Delete Bill
    path('bill/delete/<str:bill_id>/', views.delete_bill, name='delete_bill'),

    # Edit Bill
    path('bill/edit/<str:bill_id>/', views.edit_bill, name='edit_bill'),

    # Print Bill
    path('bill/print/<str:bill_id>/', views.print_bill, name='print_bill'),

    # Load Messages
    path('messages/', views.load_messages, name='load_messages'),

    # NEW: Barcode API endpoint
    path('api/product-by-barcode/<str:barcode>/', views.get_product_by_barcode, name='product_by_barcode'),
]