from django.db import models

# Create your models here.


class Post(models.Model):
    message = models.TextField()

    # 이것도 관리자 화면에서 활용이 가능하다. verbose_name으로 설정되는 값은
    # 관리자 화면에서의 카테고리 명, 관리자 화면을 통한 데이터 생성 혹은 수정시의 이름으로 활용된다.
    is_public = models.BooleanField(default=False, verbose_name='공개여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Java의 toString
    def __str__(self):
        # return f'Post object ({self.id})'
        return self.message

    # 기본적으로 임의 정의 함수의 경우에는 받는 인자가 self이외에는 있어서는 안된다고 한다.
    # 확실한건 다른곳에서도 쓰일수 있겠지만, 같은 app 단위 안에서 admin.py가 사용이 가능하다.
    def message_length(self):
        return len(self.message)

    # 00(정의함수).short_description = 'admin페이지에서 보고싶은 카테고리 명'
    # 이어서 이건 "카테고리 명"을 정의하는 것이고, 해당 카테고리에 딸려있는 content에 대한
    # 글씨 정의는 admin.py에서 진행한다.
    message_length.short_description = '메세지 글자수'
