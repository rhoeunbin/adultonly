from multiprocessing import AuthenticationError
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.
def main(request):
    return render(request, 'accounts/main.html')
    
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:main')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
    }

    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)

            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect('accounts:main')
        else:
            form = AuthenticationForm()
        
        context = {
            'form' : form
        }
        return render(request, 'accounts/login.html', context)
    else:
        return redirect('accounts:main')

def logout(request):
    auth_logout(request)
    return redirect('accounts:main')
