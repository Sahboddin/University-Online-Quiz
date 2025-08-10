# account/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # optionally auto-login after signup:
            login(request, user)
            return redirect('quiz:list')   # change to desired url name
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})

@login_required
def profile_view(request):
    # simple placeholder for logged-in user's profile page
    return render(request, 'account/profile.html', {})
