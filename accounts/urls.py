from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('detail/', views.detail, name='detail'),
    path('update/', views.update, name='update'),
]