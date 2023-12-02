from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def myview(request):
    context={
        "username":request.user.username,
        "email": request.user.email,
        }
    return render(request,'account/account.html',context)
