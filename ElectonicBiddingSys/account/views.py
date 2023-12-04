from django.shortcuts import render
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
    SQL='SELECT i.name, i.description, b.Price FROM Bid b JOIN Item i ON b.ItemId = i.ItemId WHERE b.userId ='+str(id)
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
    
            
