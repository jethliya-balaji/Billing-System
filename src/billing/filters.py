import django_filters
from .models import Bill
from django import forms
from django.db import models


class BillFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all_fields', label="Search")
    date = django_filters.DateFilter(field_name='date', widget=forms.DateInput(attrs={'type': 'date'}), lookup_expr='date__exact')

    class Meta:
        model = Bill
        fields = ['date', 'billed_by', 'search']

    def filter_by_all_fields(self, queryset, name, value):
        """
        Filter by customer_name or id using a single search box.
        """
        return queryset.filter(
            models.Q(customer_name__icontains=value) | models.Q(
                id__icontains=value)
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['billed_by'].empty_label = "Bill By"
        self.form.fields['search'].widget.attrs.update({'placeholder': 'Search by Customer Name or Bill No.'})
