from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("board/", views.board, name="board"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/likes", views.likes, name="likes"),
    path("create/", views.create, name="create"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path(
        "<int:pk>/comments/<int:comment_pk>/delete/",
        views.delete_comment,
        name="delete_comment",
    ),
]
