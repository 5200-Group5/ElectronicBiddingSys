from django.shortcuts import render, get_object_or_404, redirect
from bidding.models import Item, Bid  # Import your Item model
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation

# Create your views here.
def bidding_page(request):
    items = Item.objects.all()  # Get all items from the database
    return render(request, 'bidding/bidding_page.html', {'items': items})

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    print(f"Debug: item.id = {item.item_id}")  # Add this line for debugging
    return render(request, 'bidding/item_detail.html', {'item': item})

def place_bid(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount', None)
        
        # Convert bid_amount to the appropriate data type (e.g., Decimal)
        # and validate (ensure it's greater than the starting price and higher than the current highest bid)
        try:
            bid_amount = Decimal(bid_amount)
        except (TypeError, InvalidOperation):
            return HttpResponse("Invalid bid amount", status=400)

        if bid_amount < item.starting_price:
            return HttpResponse("Bid must be higher than starting price", status=400)

        # Check if bid is higher than the current highest bid (if applicable)
        # ...

        # Create and save the bid
        bid = Bid(item=item, user=request.user, amount=bid_amount)
        bid.save()

        # Redirect to item detail page or another success page
        return redirect(reverse('item_detail', args=[item_id]))

    # If not a POST request, redirect to item detail page or show an error
    return redirect(reverse('item_detail', args=[item_id]))