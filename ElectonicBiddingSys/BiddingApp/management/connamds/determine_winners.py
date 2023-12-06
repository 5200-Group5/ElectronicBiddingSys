from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import Item, Bid

class Command(BaseCommand):
    help = 'Determine and update winners for items whose end times have passed.'

    def handle(self, *args, **kwargs):
        current_time = timezone.now()
        items_to_update = Item.objects.filter(end_date__lt=current_time, winner__isnull=True)

        for item in items_to_update:
            winning_bid = Bid.objects.filter(item=item).order_by('-price').first()
            if winning_bid:
                item.winner = winning_bid.user
                item.save()
                self.stdout.write(self.style.SUCCESS(f"Winner determined for item '{item.name}': {winning_bid.user.username}"))
            else:
                self.stdout.write(self.style.WARNING(f"No winner found for item '{item.name}'"))
