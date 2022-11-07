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
            "address" : "주소",
            "address_detail" : "상세 주소",
        }
        widgets = {
            'address' : forms.TextInput(attrs={"class": "form-control", "id": "address_kakao", "placeholder": "주소"} ),
            'address_detail' : forms.TextInput(attrs={"class": "form-control", "name" :"address_detail", "placeholder": "상세 주소" })           
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

# class TagForm(forms.ModelForm):
#     class Meta:
#         model= Tag
#         fields=['name']