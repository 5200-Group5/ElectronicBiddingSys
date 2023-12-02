# from django.shortcuts import render, redirect
# from .forms import UserCreationForm
# from django.contrib.auth import authenticate, login
# from django.contrib import messages
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.decorators import login_required
# # Create your views here.


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Redirect to a success page or login page
#             return redirect('login')
#     else:
#         form = UserCreationForm()

#     return render(request, 'registration/register.html', {'form': form})


# def sign_in(request):
#     # Redirect to home if already authenticated
#     if request.user.is_authenticated:
#         return redirect('home')  # Replace 'home' with your home page's URL name

#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('home')  # Redirect to home page after successful sign in
#             else:
#                 messages.error(request, 'Invalid username or password.')
#         else:
#             messages.error(request, 'Invalid username or password.')

#     else:
#         form = AuthenticationForm()

#     return render(request, 'registration/login.html', {'form': form})

from django.shortcuts import render
from django_filters.views import FilterView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import Category, Item

# Create your views here.


class ItemFilterView(FilterView):
    model = Item
    template_name = "BiddingApp/item_list.html"
    filterset_fields = {
        "category": ["exact"],
        "name": ["icontains"],
    }
    paginate_by = 10
    ordering = ["name"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context["filter"].form
        form.helper = FormHelper()
        form.helper.form_method = "GET"
        form.helper.form_action = "."
        form.helper.form_class = 'form-horizontal'
        form.helper.label_class = 'col-lg-4'
        form.helper.field_class = 'col-lg-8'
        form.helper.layout = Layout(
            Row(
                Column("category", css_class="form-group col-md-4 mb-0"),
                Column("name__icontains", css_class="form-group col-md-4 mb-0"),
                Column(Submit("submit", "Filter", css_class="btn btn-primary"), css_class="form-group col-md-4 mb-0")),
        )
        return context

from django.shortcuts import render, get_object_or_404, redirect
from BiddingApp.models import Item, Bid  # Import your Item model
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation

# Create your views here.
def bidding_page(request):
    items = Item.objects.all()  # Get all items from the database
    return render(request, 'BiddingApp/bidding_page.html', {'items': items})

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    print(f"Debug: item.id = {item.item_id}")  # Add this line for debugging
    return render(request, 'BiddingApp/item_detail.html', {'item': item})

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