from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


# Create your models here.
class Restaurant(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    address = models.TextField()
    address_detail = models.TextField()
    image = models.ImageField(upload_to="articles/", blank=True)
    grade = models.FloatField()
    food_type = models.CharField(max_length=80)
    opening_hours = models.TextField()
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_restaurant"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ArticleComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    content = models.TextField()
    image = models.ImageField(upload_to="review/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 유저, 추천 추가하기 이미지 여러개 모델 추가해서 fk 넣기
