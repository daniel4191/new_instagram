from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # auto_now_add는 생성일자
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now는 수정일자
    updated_at = models.DateTimeField(auto_now=True)