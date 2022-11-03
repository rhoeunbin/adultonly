from .models import Restaurant, ArticleComment as Comment
from django import forms


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            "title",
            "content",
            "image",
            "address",
            "address_detail",
        ]
        labels = {
            "title": "가게명",
            "content": "가게 정보",
            "image": "사진",
        }
        widgets = {
            'address' : forms.TextInput(attrs={"class": "form-control", "id": "address_kakao"}),
            'address_detail' : forms.TextInput(attrs={"class": "form-control", "name" :"address_detail" })           
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
