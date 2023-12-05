from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm
from django.contrib.auth.models import User

@login_required
def send_message(request, username):
    recipient = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user 
            message.receiver = recipient
            message.save()  
            return render(request, 'message/message_sent.html', {'recipient': recipient})
    else:
        form = MessageForm()
    
    return render(request, 'message/send_message.html', {'form': form, 'recipient': recipient})


# def save_message(request):
#     if request.method == 'POST':
#         form = MessageForm(request.POST, request.FILES) 
#         if form.is_valid():
#             form.save()  
#             return redirect('message:send_message')  
#     else:
#         form = MessageForm()  

#     return render(request, 'message/send_message.html', {'form': form})

@login_required
def view_message(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'message/view_message.html', {'messages': messages})
