from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page  # <-- NEW
from .models import Message

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html')

@cache_page(60)  # <-- NEW: Cache for 60 seconds
@login_required
def threaded_conversation(request):
    root_messages = Message.objects.filter(
        sender=request.user,
        parent_message=None
    ).select_related('sender', 'receiver')\
     .prefetch_related('replies__sender', 'replies__receiver')

    return render(request, 'threaded.html', {'messages': root_messages})

@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.for_user(request.user).only('id', 'sender', 'content', 'timestamp')
    return render(request, 'unread_messages.html', {'messages': unread_messages})
