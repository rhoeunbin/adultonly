from multiprocessing import AuthenticationError
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
def main(request):
    return render(request, "accounts/main.html")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            if request.POST.get("job") == "2":
                user_form.is_staff = True
            elif request.POST.get("job") == "1":
                user_form.is_user = True
            form.save()
            return redirect("accounts:main")
    else:
        form = CustomUserCreationForm()

    context = {
        "form": form,
    }

    return render(request, "accounts/signup.html", context)


def login(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect(request.GET.get("next") or "accounts:main")
        else:
            form = AuthenticationForm()

        context = {"form": form}
        return render(request, "accounts/login.html", context)
    else:
        return redirect("accounts:index")


def logout(request):
    auth_logout(request)
    return redirect("accounts:main")


def index(request):
    users = get_user_model().objects.all()
    context = {
        "users": users,
    }
    return render(request, "accounts/index.html", context)


def profile(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {"user": user}
    return render(request, "accounts/profile.html", context)


@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("accounts:index")
    else:
        form = PasswordChangeForm(request.user)
    context = {"form": form}
    return render(request, "accounts/change_password.html", context)


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("articles:index")


@login_required
def follow(request, pk):
    user = get_user_model().objects.get(pk=pk)

    if request.user == user:
        return redirect("accounts:profile", pk)
    if request.user in user.followers.all():
        user.followings.remove(request.user)
    else:
        user.followings.add(request.user)
    return redirect("accounts:profile", pk)


def naverlogin(request):
    return render(request, "accounts/naverlogin.html")


import secrets

state_token = secrets.token_urlsafe(16)


def kakao_request(request):
    kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
    redirect_uri = "http://localhost:8000/accounts/login/kakao/callback"
    client_id = "72b73a1d5e11f6c8e5ebb51f86c0dfab"  # 배포시 보안적용 해야함
    return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


def kakao_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": "72b73a1d5e11f6c8e5ebb51f86c0dfab",  # 배포시 보안적용 해야함
        "redirect_uri": "http://localhost:8000/accounts/login/kakao/callback",
        "code": request.GET.get("code"),
    }
    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    access_token = requests.post(kakao_token_api, data=data).json()["access_token"]

    headers = {"Authorization": f"bearer ${access_token}"}
    kakao_user_api = "https://kapi.kakao.com/v2/user/me"
    kakao_user_information = requests.get(kakao_user_api, headers=headers).json()

    kakao_id = kakao_user_information["id"]
    kakao_nickname = kakao_user_information["properties"]["nickname"]
    kakao_profile_image = kakao_user_information["properties"]["profile_image"]

    if get_user_model().objects.filter(kakao_id=kakao_id).exists():
        kakao_user = get_user_model().objects.get(kakao_id=kakao_id)
    else:
        kakao_login_user = get_user_model()()
        kakao_login_user.username = kakao_nickname
        kakao_login_user.kakao_id = kakao_id
        kakao_login_user.set_password(str(state_token))
        kakao_login_user.save()
        kakao_user = get_user_model().objects.get(kakao_id=kakao_id)
    auth_login(request, kakao_user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect(request.GET.get("next") or "accounts:index")


def naver_request(request):
    naver_api = "https://nid.naver.com/oauth2.0/authorize?response_type=code"
    client_id = "mwAzJRdaHS860HumilZ7"  # 배포시 보안적용 해야함
    redirect_uri = "http://localhost:8000/accounts/login/naver/callback"
    state_token = secrets.token_urlsafe(16)
    return redirect(
        f"{naver_api}&client_id={client_id}&redirect_uri={redirect_uri}&state={state_token}"
    )


def naver_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": "mwAzJRdaHS860HumilZ7",  # 배포시 보안적용 해야함
        "client_secret": "Aa7AEd9pZ6",
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "redirect_uri": "http://localhost:8000/accounts/login/naver/callback",
    }
    naver_token_request_url = "https://nid.naver.com/oauth2.0/token"
    access_token = requests.post(naver_token_request_url, data=data).json()[
        "access_token"
    ]

    headers = {"Authorization": f"bearer {access_token}"}
    naver_call_user_api = "https://openapi.naver.com/v1/nid/me"
    naver_user_information = requests.get(naver_call_user_api, headers=headers).json()

    naver_id = naver_user_information["response"]["id"]
    naver_nickname = naver_user_information["response"]["nickname"]

    if get_user_model().objects.filter(naver_id=naver_id).exists():
        naver_user = get_user_model().objects.get(naver_id=naver_id)
    else:
        naver_login_user = get_user_model()()
        naver_login_user.username = naver_nickname
        naver_login_user.naver_id = naver_id
        naver_login_user.set_password(str(state_token))
        naver_login_user.save()
        naver_user = get_user_model().objects.get(naver_id=naver_id)
    auth_login(request, naver_user, backend="django.contrib.auth.backends.ModelBackend")

    return redirect(request.GET.get("next") or "accounts:index")
