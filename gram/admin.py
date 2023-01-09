from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Comment
# Register your models here.

# admin 구현 방법1
# admin.site.register(Post)

# admin 구현 방법2
# class PostAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Post, PostAdmin)

# admin 구현 방법3
# 굳이 이 방법으로 왜 사용할까?


@admin.register(Post)  # Wrapping
class PostAdmin(admin.ModelAdmin):
    # list_display는 일종의 내장 함수로써 이름이 이미 정해진 것 같다.
    # 이것은 관리자 화면에서 볼때의 카테고리를 지정해주는 것이다.
    list_display = ['id', 'photo_tag', 'message',
                    'message_length', 'is_public', 'created_at', 'updated_at']
    # links는 사용하기에 따라서는 활용도 가능하겠지만, 기본적으로는 여기 등록되어있는 필드값은
    # 눌러서 수정이 가능하다. (관리자 페이지에서)
    list_display_links = ['message']

    # 관리자 화면에서 등호(=)를 기준으로 오른쪽에 놓인 값을 기준으로 검색해준다. 는 기능이다.
    search_fields = ['message']

    # 관리자 화면에서 등호(=)를 기준으로 오른쪽에 놓인 값을 기준으로 필터를 생성해준다. 라는 기능이다.
    list_filter = ['created_at', 'is_public']

    def photo_tag(self, post):
        if post.photo:
            # mark_safe는 '보안상 안전하다. 그러니깐 이 이미지를 그대로 보여줘도 된다.' 뭐 그런뜻임.
            return mark_safe(f'<img src="{post.photo.url}" style="width: 72px;">')
        return None

    # 관리자페이지에서 볼때, 카테고리명은 이미 models.py에서 지정이 되었고
    # 이것은 해당 카테고리명에 딸려오는 데이터 필드에 대한 내용을 커스텀 해주는 것이다.
    # 여기서 쓰이는 post 소문자는 Post 모델을 받아온 것이다.
    def message_length(self, post):
        return f'{len(post.message)} 글자'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
