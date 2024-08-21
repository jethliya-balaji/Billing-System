from django.core.management.base import BaseCommand
from django.utils import timezone
from billing.models import Bill

class Command(BaseCommand):
    help = 'Deletes bills with no items that are not from today'

    def handle(self, *args, **options):
        today = timezone.now().date()
        
        # Get bills that are not from today and have no items
        bills_to_delete = Bill.objects.filter(
            date__date__lt=today,
            items__isnull=True
        )
        
        # Count the bills to be deleted
        count = bills_to_delete.count()
        
        # Delete the bills
        bills_to_delete.delete()
        
        if count > 0:
            self.stdout.write(self.style.SUCCESS(f"Succesfully deleted {count} bills"))
        else:
            self.stdout.write(self.style.SUCCESS("No bills to delete"))