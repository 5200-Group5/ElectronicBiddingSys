from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST
from .models import ReportedIssue, transaction
from .forms import ReportForm, PayForm


@login_required
def myview(request):
    context={
        "username":request.user.username,
        "email": request.user.email,
        }
    return render(request,'account/account.html',context)

def history(request):
    id=request.user.id
    cursor = connection.cursor()
    SQL='SELECT distinct i.name, i.description, b.Price FROM Bid b JOIN Item i ON b.ItemId = i.ItemId WHERE b.userId ='+str(id)
                # Execute SQL queries
    cursor.execute(SQL)
    result = cursor.fetchall()
    context={
            "item_list":result,
            }
    if len(result)==0:
        return render(request,'account/nothing.html',context)
    else:
        return render(request, 'account/history.html', context)
    
def create_report(request):
    form = ReportForm()
    return render(request, 'account/create_report.html', {'form': form})

def save_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)  # Include request.FILES if your form contains file uploads like images
        if form.is_valid():
            form.save()  # Save the new item to the database
            return redirect('account:account')  
    else:
        form = ReportForm()  # If not POST, create a blank form

    return render(request, 'account/create_report.html', {'form': form})

def create_payment(request):
    form = PayForm()
    return render(request, 'account/create_payment.html', {'form': form})

def save_payment(request):
    if request.method == 'POST':
        form = PayForm(request.POST, request.FILES)  # Include request.FILES if your form contains file uploads like images
        if form.is_valid():
            form.save()  # Save the new item to the database
            return redirect('account:history')  
    else:
        form = PayForm()  # If not POST, create a blank form

    return render(request, 'account/create_payment.html', {'form': form})            

