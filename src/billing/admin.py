from django.contrib import admin
from .models import Product, Bill, BillItem

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'default_rate', 'barcode']
    search_fields = ['name', 'barcode']
    readonly_fields = ['barcode']

class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 1
    readonly_fields = ('get_default_rate', 'get_total')
    fields = ('product', 'quantity', 'get_default_rate', 'custom_rate', 'get_total')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'mobile_number', 'date', 'total_amount', 'billed_by']
    list_filter = ['date', 'billed_by']
    inlines = [BillItemInline]

@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ['bill', 'product', 'quantity', 'get_default_rate', 'custom_rate', 'total']