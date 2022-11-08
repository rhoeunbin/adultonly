from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@require_safe
def board(request):
    print(request.GET.get("user"))
    page = request.GET.get("page", "1")
    posts = Post.objects.order_by("-pk")
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)
    context = {
        "posts": page_obj,
    }
    return render(request, "communities/board.html", context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    context = {
        "post": post,
        "comments": post.comment_set.all(),
        "comment_form": comment_form,
        "total_comments": post.comment_set.count(),
    }
    return render(request, "communities/detail.html", context)


@login_required
def create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "작성한 글이 등록되었습니다.")
            return redirect("communities:board")
    else:
        post_form = PostForm()
    context = {
        "post_form": post_form,
    }
    return render(request, "communities/create.html", context)


@login_required
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.user:
        if request.method == "POST":
            post_form = PostForm(request.POST, request.FILES, instance=post)
            if post_form.is_valid():
                post_form.save()
                messages.success(request, "글이 수정되었습니다.")
                return redirect("communities:detail", post.pk)
        else:
            post_form = PostForm(instance=post)
        context = {
            "post_form": post_form,
            "post_pk": post.pk,
        }
        return render(request, "communities/update.html", context)
    else:
        messages.warning(request, "접근 권한이 없습니다.")
        return redirect("communities:detail", post.pk)


@login_required
def delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.user:
        if request.method == "POST":
            post.delete()
            messages.success(request, "글이 삭제되었습니다.")
            return redirect("communities:board")
        context = {
            "post": post,
        }
        return redirect("communities:detail", context)
    else:
        messages.warning(request, "접근 권한이 없습니다.")
        return redirect("communities:detail", post.pk)


@login_required
def create_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm(request.POST, request.FILES)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        context = {
            "content": comment.content,
            "username": comment.user.username,
        }
    return redirect("communities:detail", post.pk)


# @login_required
# def update_comment(request, pk):


@login_required
def delete_comment(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        messages.success(request, "댓글이 삭제되었습니다.")
        return redirect("communities:detail", pk)
    else:
        messages.warning(request, "작성자만 삭제할 수 있습니다.")
        return redirect("communities:detail", pk)
