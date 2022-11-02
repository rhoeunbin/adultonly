from multiprocessing import AuthenticationError
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


# Create your views here.
def main(request):
    return render(request, 'accounts/main.html')
    
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            if request.POST.get('job') == '2':
                user_form.is_staff = True
            elif request.POST.get('job') == '1':
                user_form.is_user = True
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
        return redirect('accounts:index')

def logout(request):
    auth_logout(request)
    return redirect('accounts:main')

def index(request):
    users = get_user_model().objects.all()
    context = {
        'users': users,
    }
    return render(request, 'accounts/index.html', context)

def profile(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        'user':user
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user.pk)
        else:
            form = CustomUserChangeForm(instance=request.user)
        context = {
            'form': form
        }
    return render(request, 'accounts/update.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form
    }
    return render(request, 'accounts/change_password.html', context)

@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('articles:index')

@login_required
def follow(request, pk):
    user = get_user_model().objects.get(pk=pk)

    if request.user == user:
        return redirect('accounts:profile', pk)
    if request.user in user.followers.all():
        user.followings.remove(request.user)
    else:
        user.followings.add(request.user)
    return redirect('accounts:profile',pk)