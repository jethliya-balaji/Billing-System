from django import forms
from .models import Bill, BillItem

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['customer_name', 'mobile_number']
        error_messages = {
            'mobile_number': {
                'invalid': 'Please enter a valid mobile number',
            }
        }

class BillItemForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, required=True)
    class Meta:
        model = BillItem
        fields = ['product', 'quantity', 'custom_rate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].empty_label = "Select Product"