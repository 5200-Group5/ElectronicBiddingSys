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
# from openai import OpenAI
from .models import Category, Item
from django.db import connection


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
from .forms import ItemForm

# Create your views here.
@login_required
def bidding_page(request):
    items = Item.objects.all()  # Get all items from the database
    form = ItemForm()
    return render(request, 'BiddingApp/bidding_page.html', {'items': items})

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    bids = item.bid_set.all().order_by('-price')  # Corrected to 'price'

    if request.method == 'POST' and request.user.is_authenticated:
        bid_price = request.POST.get('bid_price', None)
        
        try:
            bid_price = Decimal(bid_price)
        except (TypeError, InvalidOperation):
            return HttpResponse("Invalid bid price", status=400)

        if bid_price <= item.starting_price:
            return HttpResponse("Bid must be higher than starting price", status=400)

        highest_bid = bids.first()
        if highest_bid and bid_price <= highest_bid.price:
            return HttpResponse("There is already a higher bid.", status=400)

        bid = Bid(item=item, user=request.user, price=bid_price)
        bid.save()

        return redirect(reverse('bidding:item_detail', args=[item_id]))

    return render(request, 'BiddingApp/item_detail.html', {'item': item, 'bids': bids})

@login_required
def place_bid(request, item_id):
    # This function might not be necessary
    pass


def create_item(request):
    form = ItemForm()
    return render(request, 'BiddingApp/create_item.html', {'form': form})

def save_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)  # Include request.FILES if your form contains file uploads like images
        if form.is_valid():
            form.save()  # Save the new item to the database
            return redirect('bidding:bidding_page')  # Redirect to bidding page or another appropriate page

    else:
        form = ItemForm()  # If not POST, create a blank form

    return render(request, 'BiddingApp/create_item.html', {'form': form})



api_key = " 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"
openAIDescription = "This is sql database with 3 tables, and the first table name is Item, "\
                    "the columns name are ItemID, Description,Picture,Category(two type 'Antiques' and 'Electronics')" \

                    "Cond(it contains two type Used and New), Starting_price, End_date,Start_date " \
                    "The second table name is auth_user,the columns name are id,password,last_login,is_superuser,"\
                    "username,first_name,last_name, email, is_staff, is_active, date_joined "\
                    "The third table name is Bid, the columns name are BidID,ItemID,UserID,Price,Status"\
                    "I will give you description of what I want to search from the database, and you should give me a "\
                     "SQL query to find them."\


from django.shortcuts import render
from openai import OpenAI
import json
# 您的视图函数

def chatbot(request):


    if api_key is not None and request.method == 'POST':
        client = OpenAI(
            api_key=api_key
        )

        user_input = request.POST.get('user_input')
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": user_input
                }
            ],
            model="gpt-3.5-turbo",
            functions=[
                {
                    "name": "query_database",
                    "description": user_input,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql": {
                                "type": "string",
                                "description": openAIDescription,
                            },
                        },
                        "required": ["sql"],
                    },
                }
            ],
            function_call='none',
        )

        sql_message = response.choices[0].message.content
        print(sql_message)
        start_index = sql_message.find('{')
        end_index = sql_message.find('}', start_index)
        print(start_index)
        print(end_index)
        if start_index != -1 and end_index != -1:
            sql_json = str(sql_message[start_index:end_index+1])
            print(sql_json)
        else:
            sql_json = None

        if sql_json is not None:
            try:
                json_object = json.loads(sql_json)
            except Exception as e:
                print("wrong")
                sql_data = ["Failed, GPT gives a wrong SQL query from your search"]
                return render(request, 'chatbox.html', {'chatbox_data': sql_data})
        else:
            print("no sql_json")
            sql_data = ["Failed, GPT didn't return a SQL query from your search"]
            return render(request, 'chatbox.html', {'chatbox_data': sql_data})

        sql = json_object["sql"]
        try:
            sql_data = SQLQuery(sql)
        except ValueError as ve:
            print("fail")
        except OperationalError as e:
            print("fail")
        except Exception as e:
            print("fail")

        if not sql_data:
            sql_data = ["Noting found in database"]
        return render(request, 'chatbox.html', {'chatbox_data': sql_data})
    else:
        return render(request, 'chatbox.html', {})

def SQLQuery(sql_query):
    if not sql_query:
        raise ValueError("SQL query must be a non-empty string")
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        results = cursor.fetchall()
    return results