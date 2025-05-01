import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db import transaction
from django.core.exceptions import ValidationError
from decimal import Decimal


class Product(models.Model):
    name = models.CharField(max_length=100)
    default_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    purchase_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0, null=True, blank=True)
    barcode = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-generate barcode if not provided
        if not self.barcode:
            self.barcode = self.generate_barcode()
        super().save(*args, **kwargs)
    
    def generate_barcode(self):
        """Generate a unique barcode for the product"""
        # Get the current date in YYMMDD format
        from django.utils import timezone
        date_prefix = timezone.now().strftime("%y%m%d")
        
        # Generate a random 6-digit number
        random_part = ''.join(random.choices(string.digits, k=6))
        
        # Combine to form a barcode: date + random digits
        barcode = f"{date_prefix}{random_part}"
        
        # Ensure uniqueness
        while Product.objects.filter(barcode=barcode).exists():
            random_part = ''.join(random.choices(string.digits, k=6))
            barcode = f"{date_prefix}{random_part}"
            
        return barcode    

    def __str__(self):
        return f"{self.name} - {self.default_rate}"


class Bill(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$')], null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0)
    billed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bills')

    def save(self, *args, **kwargs):
        customer_name = self.customer_name.title() if self.customer_name else None
        self.customer_name = customer_name
        if not self.id:
            with transaction.atomic():
                self.id = self.generate_id()
        super().save(*args, **kwargs)
        self.update_total_amount()

    def generate_id(self):
        date = timezone.now().strftime("%d%m%Y")
        random_part = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=4))
        return f"{date}-{random_part}"

    def update_total_amount(self):
        total = sum(item.total for item in self.items.all())
        self.total_amount = total
        super().save(update_fields=['total_amount'])

    def __str__(self):
        return f"Bill No. {self.id}"


class BillItem(models.Model):
    DISCOUNT_CHOICES = [
        (0, 'No Discount'),
        (40, '40% Off'),
        (50, '50% Off'),
        (-1, 'Custom')  # -1 indicates custom discount
    ]
    
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    custom_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_type = models.IntegerField(choices=DISCOUNT_CHOICES, default=0)
    custom_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Enter discount percentage")

    def clean_custom_rate(self):
        if self.custom_rate is None and (self.product.default_rate is None or self.product.default_rate == 0):
            raise ValidationError(
                "Default rate is not provided in the product. Please provide a custom rate or set a default rate."
            )

    def save(self, *args, **kwargs):
        self.clean_custom_rate()
        rate = self.custom_rate if self.custom_rate is not None else self.product.default_rate
        
        # Calculate discount
        if self.discount_type == -1 and self.custom_discount:  # Custom discount
            discount_percentage = self.custom_discount
        else:  # Fixed discount or no discount
            discount_percentage = Decimal(str(self.discount_type))  # Convert to Decimal
        
        # Apply discount
        if discount_percentage > 0:
            discount_multiplier = (Decimal('100') - discount_percentage) / Decimal('100')
            rate = rate * discount_multiplier
            
        self.total = rate * Decimal(str(self.quantity))  # Convert quantity to Decimal
        super().save(*args, **kwargs)
        self.bill.update_total_amount()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.bill.update_total_amount()

    def get_rate(self):
        return self.custom_rate if self.custom_rate is not None else self.product.default_rate

    def get_default_rate(self):
        return self.product.default_rate

    def get_total(self):
        return self.total

    get_total.short_description = 'Total'

    get_default_rate.short_description = 'Default Rate'

    def __str__(self):
        return f"{self.product.name}"
