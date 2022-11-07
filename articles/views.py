from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe
from .models import Restaurant, ArticleComment as Comment
from .forms import RestaurantForm, CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import get_latitude_longitude
from django.http import JsonResponse
import os
import dotenv
from django.contrib import messages
from django.contrib.auth.decorators import login_required


dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
# from django.contrib.auth.decorators import login_required

# Create your views here.
@require_safe
def index(request):
    return render(request, "articles/index.html")


def home(request):
    restaurants_1 = Restaurant.objects.order_by("-like_users")[:3]
    restaurants_2 = Restaurant.objects.order_by("-like_users")[3:6]
    restaurants_3 = Restaurant.objects.order_by("-like_users")[6:9]
    restaurants_4 = Restaurant.objects.order_by("-like_users")[9:12]
    context = {
        "restaurants_1": restaurants_1,
        "restaurants_2": restaurants_2,
        "restaurants_3": restaurants_3,
        "restaurants_4": restaurants_4,
    }
    return render(request, "articles/home.html", context)


def board_filter(request, pk):
    restaurants = Restaurant.objects.filter(cusine_code=pk).order_by("-pk")
    page = request.GET.get("page")
    paginator = Paginator(restaurants, 6)
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)
    print(page_obj)
    context = {
        "restaurants": page_obj,
    }
    return render(request, "articles/board.html", context)


def board(request):

    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get("code"))
    #     print("데이터가 왜 안와")
    #     restaurants = Restaurant.objects.filter(cusine_code=request.POST.get("code")).order_by("-pk")
    #     context = {
    #         'restaurants': list(restaurants.values()),
    #     }
    #     return JsonResponse(context)
    # else:
    restaurants = Restaurant.objects.order_by("-pk")
    page = request.GET.get("page")
    paginator = Paginator(restaurants, 6)
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)
    print(page_obj)
    context = {
        "restaurants": page_obj,
    }
    return render(request, "articles/board.html", context)


@login_required
def detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    lat, lon = get_latitude_longitude(restaurant.address)
    form = CommentForm(request.POST, request.FILES or None)
    client_id = os.environ["id"]
    data = {}
    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.restaurant = restaurant
            comment.user = request.user
            comment.save()
        return redirect("articles:detail", restaurant.pk)

    reviews = restaurant.articlecomment_set.values()
    avg_rating = 0
    if reviews:
        avg_rating = sum([x["rating"] for x in reviews]) // len(reviews)

    context = {
        "restaurant": restaurant,
        "comments": restaurant.articlecomment_set.all().order_by("-created_at"),
        "comment_form": form,
        "latitude": lat,
        "longitude": lon,
        "client_id": client_id,
        "avg_rating": avg_rating,
    }

    return render(request, "articles/detail.html", context)


@login_required
def create(request):
    if request.method == "POST":
        restaurant_form = RestaurantForm(request.POST, request.FILES)
        if restaurant_form.is_valid():
            restaurant = restaurant_form.save(commit=False)
            restaurant.user = request.user
            restaurant.save()
            messages.success(request, "맛집으로 등록되었습니다.")
            return redirect("articles:board")
    else:
        restaurant_form = RestaurantForm()
    context = {
        "restaurant_form": restaurant_form,
    }
    return render(request, "articles/create.html", context)


# @login_required
def update(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.user == restaurant.user:
        if request.method == "POST":
            restaurant_form = RestaurantForm(
                request.POST, request.FILES, instance=restaurant
            )
            if restaurant_form.is_valid():
                restaurant_form.save()
                messages.success(request, "맛집 정보가 수정되었습니다.")
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


def delete_comment(request, pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("articles:detail", pk)


def likes(request):
    if request.user.is_authenticated:
        restaurant = get_object_or_404(Restaurant, pk=request.POST.get("pk"))

        if restaurant.like_users.filter(pk=request.user.pk).exists():
            restaurant.like_users.remove(request.user)
            is_liked = False

        else:
            restaurant.like_users.add(request.user)
            is_liked = True
        context = {
            "is_liked": is_liked,
            "likeCount": restaurant.like_users.count(),
        }
        return JsonResponse(context)


def search_results(request):
    if request.is_ajax():
        res = None
        restaurant = request.POST.get("restaurant")
        kw = Restaurant.objects.filter(title__icontains=restaurant)
        if len(kw) > 0 and len(restaurant) > 0:
            data = []
            for k in kw:
                item = {
                    "pk": k.pk,
                    "title": k.title,
                    "address": k.address + " " + k.address_detail,
                    "phone_number": k.phone_number,
                    "image": str(k.image),
                }
                data.append(item)
            res = data
        else:
            res = "검색결과가 없습니다."
        return JsonResponse(
            {
                "restaurant": res,
            }
        )
    return JsonResponse({})


def aboutus(request):
    return render(request, "articles/aboutus.html")


@login_required
def create_comment(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.restaurant = restaurant
        comment.user = request.user
        comment.save()
    return redirect("articles:detail", restaurant.pk)
