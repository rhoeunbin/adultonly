from django.db import models
from django.conf import settings

# Create your models here.
class Restaurant(models.Model):
    title = models.CharField(max_length=80)
    address = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True)
    # img_path = models.URLField()
    food_type = models.CharField(max_length=80)
    opening_hours = models.TextField()
    grade = models.FloatField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_restaurant')
    # user, 좋아요 추가하기


# class Comment(models.Model):
#     article = models.ForeignKey("Article", on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     # 유저, 추천
