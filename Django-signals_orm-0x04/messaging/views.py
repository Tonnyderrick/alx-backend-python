from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)  # Log out before deletion
        user.delete()    # Triggers post_delete signal
        return redirect('home')  # Redirect to homepage or login

    return render(request, 'confirm_delete.html')  # A template for confirmation
