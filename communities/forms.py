from .models import Post, Comment
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
        ]
        labels = {
            "title": "제목",
            "content": "내용",
            "image": "사진 첨부",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "user" "content",
            "image",
        ]
        labels = {
            "content": "댓글",
            "image": "사진 첨부",
        }
