import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django.db import transaction
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=100)
    default_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.default_rate}"


class Bill(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=10, validators=[
                                     RegexValidator(r'^\d{10}$')], null=True, blank=True)
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
    bill = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    custom_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def clean(self):
        if self.custom_rate is None and (self.product.default_rate is None or self.product.default_rate == 0):
            raise ValidationError(
                "Default rate is not provided in the product. Please provide a custom rate or set a default rate."
            )

    def save(self, *args, **kwargs):
        self.clean()
        rate = self.custom_rate if self.custom_rate is not None else self.product.default_rate
        self.total = rate * self.quantity
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
