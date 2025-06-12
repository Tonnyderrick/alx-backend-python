from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Message

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html')

@login_required
def threaded_conversation(request):
    root_messages = Message.objects.filter(parent_message=None).select_related('sender', 'receiver')\
        .prefetch_related('replies__sender', 'replies__receiver')
    return render(request, 'threaded.html', {'messages': root_messages})
