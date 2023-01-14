from django.conf import settings
from django.db import models

# Create your models here.


class Post(models.Model):
    # related_name이 '+'라고 해놓은 것은 포기선언이다.
    # 현재 시점에서는 gram.models의 Post와 충돌이 생기기 때문이다.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    title = models.CharField(max_length=100)
    content = models.TextField()
    # auto_now_add는 생성일자
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now는 수정일자
    updated_at = models.DateTimeField(auto_now=True)
