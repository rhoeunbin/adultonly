from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path("board/", views.board, name="board"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/likes", views.likes, name="likes"),
    path("create/", views.create, name="create"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
]
