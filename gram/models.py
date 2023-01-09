from django.conf import settings
from django.db import models
# 이거는 권장되는 방법은 아니다. 이유는, User 모델은 가변적 요소이기 때문이다.
# 혹여 사용하기를 원한다면 프로젝트 단위의 settings.py의 맨 밑에 AUTH_USER_MODEL = '<앱단위이름>.User'
# 이렇게 등록해준다.
# from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    # ImageField를 사용하려면 pip install pillow를 해줘야한다.
    # black=True의 의미는 해당 필드를 '옵션 필드'즉, 할수도 있고 안할수도있고 사용자 마음대로 한다는 뜻

    # upload_to는 저장 경로를 이렇게 하겠다는 설정값을 의미한다.
    # 각 %Y, %m 이런거는 연 2자리, 월 2자리 같은것을 의미함.
    # 이거는 초단위까지 쪼개서 폴더를 지정해주겠다는 의미고 (데이터가 정말 많을때는 최소한 분단위 까지는 좋은것같다.)
    # photo = models.ImageField(blank=True, upload_to= 'gram/post/%Y/%m/%d/%H/%M/%S')
    # 이거는 각 날별로 쪼개서 폴더를 지정해주겠다는 의미
    # 근데 사실상 이것도 가장 메인이 되는 MEDIA_ROOT를 settings에 어디로 지정하냐에 따라서
    # ROOT>upload_to의 경로 순으로 배정이 된다.

    # upload_to의 인자로 오는 것은 '문자열로 경로를 리턴한다면 함수도 사용이 가능하다'
    # 즉, if 조건에 따라서 경로를 달리해줄수도 있는거다.
    photo = models.ImageField(blank=True, upload_to='gram/post/%Y%m%d')

    # 이것도 관리자 화면에서 활용이 가능하다. verbose_name으로 설정되는 값은
    # 관리자 화면에서의 카테고리 명, 관리자 화면을 통한 데이터 생성 혹은 수정시의 이름으로 활용된다.
    is_public = models.BooleanField(default=False, verbose_name='공개여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Java의 toString
    def __str__(self):
        # return f'Post object ({self.id})'
        return self.message

    class Meta:
        ordering = ['-id']

    # 기본적으로 임의 정의 함수의 경우에는 받는 인자가 self이외에는 있어서는 안된다고 한다.
    # 확실한건 다른곳에서도 쓰일수 있겠지만, 같은 app 단위 안에서 admin.py가 사용이 가능하다.
    def message_length(self):
        return len(self.message)

    # 00(정의함수).short_description = 'admin페이지에서 보고싶은 카테고리 명'
    # 이어서 이건 "카테고리 명"을 정의하는 것이고, 해당 카테고리에 딸려있는 content에 대한
    # 글씨 정의는 admin.py에서 진행한다.
    message_length.short_description = '메세지 글자수'


class Comment(models.Model):
    # 버전1 이렇게 쓰이는 것이 일반이다.
    # 그리고 limit_choices_to는 가시적으로 보이는것에 있어서 필터적 제약을 거는 것이다.
    # is_public의 경우는 해당 글에대한 공개여부 이다.
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, limit_choices_to={'is_public': True})
    # 버전2 이렇게 쓰게 되면 이 클래스가 포함되어있는 app 단위 안에서의 지정된 models을 찾아준다.
    # 지금의 경우에는 "Post"이다.
    # post = models.ForeignKey('Post', on_delete=models.CASCADE)
    # 버전3 이렇게 쓰게되면 app 단위가 다르더라도 app의 이름을 직접 지정해주기 때문에 사용이 가능하다.
    # post = models.ForeignKey('blog1.Post', on_delete=models.CASCADE)

    message = models.TextField()
    # 최초 생성 (auto_now_add)
    created_at = models.DateTimeField(auto_now_add=True)
    # 업데이트 되는 순간 순간마다 (auto_now)
    updated_at = models.DateTimeField(auto_now=True)
