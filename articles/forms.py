from .models import Restaurant, Comment
from django import forms


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            "title",
            "content",
            "image",
        ]
        labels = {
            "title": "가게명",
            "content": "가게 정보",
            "image": "사진",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "title",
            "rating",
            "content",
            "image",
        ]
        labels = {
            "title": "제목",
            "rating": "평가",
            "content": "후기",
            "image": "사진",
        }

