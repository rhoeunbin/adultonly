from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:pk>', views.profile, name='profile'),
    path('update<int:pk>/', views.update, name='update'),
    path('password/', views.change_password, name="change_password"),
    path('delete/', views.delete, name='delete'),
]