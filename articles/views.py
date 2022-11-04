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
    restaurants = Restaurant.objects.all()
    context = {
        "restaurants": restaurants,
    }
    return render(request, "articles/home.html", context)


def board(request):
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
    restaurant = get_object_or_404(Restaurant, pk=pk)
    lat, lon = get_latitude_longitude(restaurant.address)
    form = CommentForm(request.POST, request.FILES or None)
    client_id = os.environ["id"]
    data = {}
    if request.is_ajax():
        if form.is_valid():
            comment = form.save(commit=False)
            comment.restaurant = restaurant
            comment.user = request.user
            comment.save()
            data["title"] = comment.title
            # comment 객체는 cleande_data 속성이 없음
            # data['title'] = comment.cleaned_data.get['title']
            data["status"] = "ok"
            print(data)
            return JsonResponse(data)
    context = {
        "restaurant": restaurant,
        "comments": restaurant.articlecomment_set.all().order_by("-created_at"),
        "comment_form": form,
        # "total_comments": restaurant.comment_set.count(),
        "latitude": lat,
        "longitude": lon,
        "client_id": client_id,
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
        context = {"is_liked": is_liked, "likeCount": restaurant.like_users.count()}
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
                    "address": k.address,
                    "image": str(k.image.url),
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
