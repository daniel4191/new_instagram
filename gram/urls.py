from django.urls import path, re_path, register_converter

from . import views
from .converters import YearConverter, MonthConverter, DayConverter

app_name = 'gram'


# YearConverter를 year이라는 이름으로 써주겠다는 의미로써
# 일종의 알리아스라고 보면 된다.
register_converter(YearConverter, 'year')

register_converter(MonthConverter, 'month')

register_converter(DayConverter, 'day')

urlpatterns = [
    # name에 지정 되는 값들은 URL Reverse를 수행할 사실상 "pattern_name"에 지정해주는 것이다.
    # pattern_name의 기본 값은 None이다.
    # URL Reverse는 html 파일에서 {% url 'gram:post_detail' post.pk %} 이런식으로 쓰이는 걸 말한다.
    path('', views.post_list, name='post_list'),
    # 이처럼 <int:pk>라는 식으로 사용하는 것을 "converter" 라고 부른다.
    # 더 정확히는 여기서는 int를 컨버터, 뒤의 pk는 views로 부터 전달받은 converter의 인자라고 보면 된다.
    path('<int:pk>/', views.post_detail, name='post_detail'),
    # 여기의 <>인자에서 먼저오는 year이 가능한 이유는 register_converter를 통해서
    # YearConverter를 year로 알리아스 처리해주었기 때문이다.

    # 그리고 이런 url에서 받는 정보는 "사전"의 형태로 두번째 인자인 views.<함수혹은 클래스네임>으로 넘어가게 된다.
    # FBV 기반의 url
    # path('archives/<year:year>/', views.archives_year)

    # CBV 기반의 url
    path('archive/', views.post_archive, name='post_archive'),

    # 기존에는 views에 post_year_archive라고 썼었으나, 내장 CBV에 대한 값이
    # post_archive_year라서 이것으로 변경해주었다.

    # 이게 영향이 있는 것인지는 모르겠으나, register_converter로 구현을 했던 내용들의 실질적 구현 방법으로
    # 이렇게 코드 진행이 되었다.
    path('archive/<year:year>/', views.post_archive_year, name='post_archive_year'),
    path('archive/<year:year>/<month:month>/',
         views.post_archive_year, name='post_archive_month'),
    path('archive/<year:year>/<month>/<day:day>/',
         views.post_archive_year, name='post_archive_day')

]
