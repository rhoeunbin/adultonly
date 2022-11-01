from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Restaurant(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    image = models.ImageField(upload_to="restaurant/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # user, 좋아요 추가하기


class Comment(models.Model):
    article = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    content = models.TextField()
    image = models.ImageField(upload_to="review/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 유저, 추천 추가하기 이미지 여러개 모델 추가해서 fk 넣기
