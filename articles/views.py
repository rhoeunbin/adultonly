from gc import get_objects
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant
from .forms import RestaurantForm, CommentForm
from django.core.paginator import Paginator

# from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request, "articles/index.html")


def home(request):
    restaurants = Restaurant.objects.all()
    context = {
        "restaurants": restaurants,
    }
    return render(request, "articles/home.html", context)


def board(request):
    page = request.GET.get("page", "1")
    restaurants = Restaurant.objects.order_by("-pk")
    paginator = Paginator(restaurants, 10)
    page_obj = paginator.get_page(page)
    context = {
        "restaurants": page_obj,
    }
    return render(request, "articles/board.html", context)


# def detail(request, pk):
#     restaurant = Restaurant.objects.get(pk=pk)
#     comment_form = CommentForm
#     page = request.GET.get("page", "1")
#     comments = restaurant.comment_set.all()
#     paginator = Paginator(comments, 5)
#     page_obj = paginator.get_page(page)
#     context = {
#         "restaurant": restaurant,
#         "comment_form": comment_form,
#         "comments": page_obj,
#         "total_comments": restaurant.comment_set.count(),
#     }
#     return render(request, "articles/detail.html", context)
def detail(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    comment_form = CommentForm()
    context = {
        "restaurant": restaurant,
        "comments": restaurant.comment_set.all(),
        "comment_form": comment_form,
        "total_comments": restaurant.comment_set.count(),
    }

    return render(request, "articles/detail.html", context)


# @login_required
def create(request):
    if request.method == "POST":
        restaurant_form = RestaurantForm(request.POST, request.FILES)
        if restaurant_form.is_valid():
            restaurant_form.save()
            return redirect("articles:board")
    else:
        restaurant_form = RestaurantForm()
    context = {
        "restaurant_form": restaurant_form,
    }
    return render(request, "articles/create.html", context)


# @login_required
def update(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    if request.method == "POST":
        restaurant_form = RestaurantForm(
            request.POST, request.FILES, instance=restaurant
        )
        if restaurant_form.is_valid():
            restaurant_form.save()
            return redirect("articles:detail", pk)
    else:
        restaurant_form = RestaurantForm(instance=restaurant)
    context = {
        "restaurant_form": restaurant_form,
        "restaurant_pk": restaurant.pk,
    }
    return render(request, "articles/update.html", context)


def delete(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    if request.method == "POST":
        restaurant.delete()
        return redirect("articles:board")
    context = {
        "restaurant": restaurant,
    }
    return redirect("articles:detail", context)


# 댓글 중복 댓글 금지 추가하기 bcuz 평점
# @login_required
def create_comment(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    comment_form = CommentForm(request.POST, request.FILES)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.restaurant = restaurant
        comment.save()
    return redirect("articles:detail", restaurant.pk)


def delete_comment(request, pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("articles:detail", pk)


def likes(request, pk):
    
    if request.user.is_authenticated:
        restaurant = get_object_or_404(Restaurant, id=pk)

        if restaurant.like_users.filter(pk=request.user.pk).exists():
            restaurant.like_users.remove(request.user)

        else:
            restaurant.like_users.add(request.user)
        return redirect('articles:detail', pk)
    return redirect('articles:detail', pk)

