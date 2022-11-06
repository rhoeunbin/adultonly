from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.main, name="main"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("index/", views.index, name="index"),
    path("<int:pk>", views.profile, name="profile"),
    path("update/", views.update, name="update"),
    path("password/", views.change_password, name="change_password"),
    path("delete/", views.delete, name="delete"),
    path("<int:pk>/follow/", views.follow, name="follow"),
    path("login/kakao/", views.kakao_request, name="kakao"),
    path("login/kakao/callback/", views.kakao_callback),
    path("login/naver/", views.naver_request, name="naver"),
    path("login/naver/callback/", views.naver_callback),
]
