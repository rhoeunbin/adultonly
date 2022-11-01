from django.shortcuts import render, redirect
from .models import Restaurant
from .forms import RestaurantForm
from django.core.paginator import Paginator

# from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "articles/index.html")


def board(request):
    page = request.GET.get("page", "1")
    restaurants = Restaurant.objects.order_by("-pk")
    paginator = Paginator(restaurants, 10)
    page_obj = paginator.get_page(page)
    context = {
        "restaurants": page_obj,
    }
    return render(request, "articles/board.html", context)


def detail(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    context = {
        "restaurant": restaurant,
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
