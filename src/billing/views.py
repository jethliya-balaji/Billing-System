from urllib.parse import urlparse
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import resolve
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib import messages


from django_htmx.http import HttpResponseClientRedirect

from .filters import BillFilter
from .forms import BillForm, BillItemForm
from .models import Bill, BillItem

# Create your views here.


@login_required
@require_GET
def dashboard(request):
    if request.user.is_superuser:
        # Get all bills that have either customer_name, mobile_number, or items
        bills = Bill.objects.filter(
            Q(customer_name__isnull=False) |
            Q(mobile_number__isnull=False) |
            Q(items__isnull=False)
        ).distinct().order_by('-date')
    else:
        # Get all bills where the user is the billed_by user
        # and the bill has either customer_name, mobile_number, or items
        bills = Bill.objects.filter(
            Q(billed_by=request.user) &
            (Q(customer_name__isnull=False) |
             Q(mobile_number__isnull=False) |
             Q(items__isnull=False))
        ).distinct().order_by('-date')

    # Calculate sales for different periods
    now = timezone.now()
    seven_day_sale = bills.filter(
        date__gte=now - timedelta(days=7)).aggregate(total=Sum('total_amount'))['total'] or 0
    one_month_sale = bills.filter(
        date__gte=now - timedelta(days=30)).aggregate(total=Sum('total_amount'))['total'] or 0
    three_month_sale = bills.filter(
        date__gte=now - timedelta(days=90)).aggregate(total=Sum('total_amount'))['total'] or 0

    bill_filter = BillFilter(request.GET, queryset=bills)

    paginator = Paginator(bill_filter.qs, 10)
    page_number = request.GET.get('page')
    bills = paginator.get_page(page_number)

    base_url = reverse('dashboard')
    query_params = request.GET.copy()
    query_params.pop('page', None)
    url_with_filters = f"{base_url}?{query_params.urlencode()}&"

    context = {
        'bill_filter_form': bill_filter.form,
        'bills': bills,
        'total_bills': bill_filter.qs.count(),
        'url_with_filters': url_with_filters,
        'seven_day_sale': seven_day_sale,
        'one_month_sale': one_month_sale,
        'three_month_sale': three_month_sale,
    }

    if request.htmx:
        return render(request, 'billing/partials/dashboard_bill.html', context)

    return render(request, 'billing/dashboard.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
@permission_required('billing.add_bill', raise_exception=True)
def create_bill(request):
    bill = Bill.objects.filter(
        Q(items__isnull=True) &
        Q(billed_by=request.user) &
        Q(date__date=timezone.now().date())
    ).first()
    if not bill:
        bill = Bill.objects.create(billed_by=request.user)

    bill_form = BillForm(instance=bill)
    bill_item_form = BillItemForm()

    if request.method == 'POST':
        bill_form = BillForm(request.POST, instance=bill)
        if bill_form.is_valid():
            bill = bill_form.save(commit=False)
            bill.billed_by = request.user
            bill.save()
            messages.success(request, 'Bill has been successfully saved.')
            return HttpResponse('- Saved.')
        else:
            messages.error(request, bill_form.errors.as_data().get('mobile_number')[0])
            return HttpResponse('- Error.')

    context = {
        'bill': bill,
        'bill_form': bill_form,
        'bill_item_form': bill_item_form,
    }

    return render(request, 'billing/create_edit_bill.html', context)


@login_required
@require_POST
@permission_required('billing.add_billitem', raise_exception=True)
def add_item(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill_item_form = BillItemForm(request.POST)
    if bill_item_form.is_valid():
        bill_item = bill_item_form.save(commit=False)
        bill_item.bill = bill
        bill_item.save()
        messages.success(request, 'Item added successfully.')

        context = {
            'items': bill.items.all(),
            'bill': bill,
        }
        return render(request, 'billing/partials/create_edit_bill_item.html', context)
    else:
        return HttpResponse(bill_item_form.errors.as_data().get('__all__')[0], status=400)


@login_required
@require_http_methods(['DELETE'])
@permission_required('billing.delete_billitem', raise_exception=True)
def delete_item(request, item_id):
    item = get_object_or_404(BillItem, id=item_id)
    bill = item.bill
    item.delete()
    messages.success(request, 'Item deleted successfully.')
    context = {
        'items': bill.items.all(),
        'bill': bill,
    }
    return render(request, 'billing/partials/create_edit_bill_item.html', context)


@login_required
@require_GET
@permission_required('billing.view_bill', raise_exception=True)
def view_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, 'billing/view_bill.html', {'bill': bill})


@login_required
@require_http_methods(['DELETE'])
@permission_required('billing.delete_bill', raise_exception=True)
def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    if bill.billed_by != request.user and not request.user.is_superuser:
        raise PermissionDenied("You are not allowed to delete this bill.")

    bill.delete()
    messages.success(request, 'Bill deleted successfully.')

    # cheack if the request is coming from the dashboard or the view bill page
    referer = resolve(urlparse(request.META.get('HTTP_REFERER')).path).url_name

    if referer == 'view_bill':
        return HttpResponseClientRedirect('/')
    elif referer == 'dashboard':
        if request.user.is_superuser:
            # Get all bills that have either customer_name, mobile_number, or items
            bills = Bill.objects.filter(
                Q(customer_name__isnull=False) |
                Q(mobile_number__isnull=False) |
                Q(items__isnull=False)
            ).distinct().order_by('-date')
        else:
            # Get all bills where the user is the billed_by user
            # and the bill has either customer_name, mobile_number, or items
            bills = Bill.objects.filter(
                Q(billed_by=request.user) &
                (Q(customer_name__isnull=False) |
                 Q(mobile_number__isnull=False) |
                 Q(items__isnull=False))
            ).distinct().order_by('-date')
        return render(request, 'billing/partials/dashboard_bill.html', {'bills': bills})
    else:
        return HttpResponseClientRedirect('/')


@login_required
@require_http_methods(['GET', 'POST'])
@permission_required('billing.change_bill', raise_exception=True)
def edit_bill(request, bill_id):

    bill = get_object_or_404(Bill, id=bill_id)

    if bill.billed_by != request.user and not request.user.is_superuser:
        return HttpResponse('You are not allowed to edit this bill.', status=403)

    bill_form = BillForm(instance=bill)
    bill_item_form = BillItemForm()

    if request.method == 'POST':
        bill_form = BillForm(request.POST, instance=bill)
        if bill_form.is_valid():
            bill = bill_form.save()
            messages.success(request, 'Bill has been successfully saved.')
            return HttpResponse('- Saved.')
        else:
            messages.error(request, bill_form.errors.as_data().get('mobile_number')[0])
            return HttpResponse('- Error.')

    context = {
        'bill': bill,
        'bill_form': bill_form,
        'bill_item_form': bill_item_form,
    }

    return render(request, 'billing/create_edit_bill.html', context)


@login_required
@require_GET
@permission_required('billing.view_bill', raise_exception=True)
def print_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, 'billing/print_bill.html', {'bill': bill})


@login_required
@require_GET
def load_messages(request):
    return render(request, 'billing/partials/messages.html')
