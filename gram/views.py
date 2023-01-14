from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.dates import ArchiveIndexView, YearArchiveView


from .models import Post

# Create your views here.

# CBV 기반 1
# 다만 딱 이렇개 한 줄만 쓰게 되면 검색이 되진 않기 때문에 추가로 구현해줘야한다.
# post_list = ListView.as_view(model=Post, paginate_by=10)

# CBV 기반 2 + 데코레이터
# name은 이건 어떤 메소드다. 라는것을 명시해주는 것
# @method_decorator(login_required, name='dispatch')
# class PostListView(ListView):
#     model = Post
# paginate_by = 10


# CBV 기반 3 + 데코레이터를 대신하여 LoginRequireMixin 사용
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10


# 이건 CBV 기반의 view를 만들때마다 urls를 만져줄 수 없으니, 그것을 대신하여 urls에 이미 post_list라고
# 등록이 되어있기 때문에 해주는 것이다.
post_list = PostListView.as_view()


# FBV 기반
# @login_required
# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get('q', '')
#     if q:
#         qs = qs.filter(message__icontains=q)
#     # gram/templates/gram/post_list.html
#     return render(request, 'gram/post_list.html', {
#         'post_list': qs,
#         'q': q
#     })


# response 방법1
'''
def post_detail(request, pk):    
    response = HttpResponse()
    response.write('hello, world')
    return response
'''

# response 방법2
# 타입 지정 (파이썬에서는 불필요하지만 이렇게 사용해주는 경우도 있다.)
"""
def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    response = HttpResponse()
    response.write('hello, world')
    return response
"""

# FBV 방법 1

"""
def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = Post.objects.get(pk=pk)
    return render(request, 'gram/post_detail.html', {
        'post': post
    })
"""
# 바로 위의 FBV 방식을 이렇게 한줄로 처리 가능하다.
# CBV 방식 1
# post_detail = DetailView.as_view(model=Post)

# CBV 방식 2
# post_detail = DetailView.as_view(
#     model=Post,
#     # is_public = True로써 공개 처리가 된 글만 볼 수 있다.
#     queryset=Post.objects.filter(is_public=True)
# )

# CBV 방식 3


class PostDetailView(DetailView):
    model = Post

    # CBV 방식 하에서 get_queryset을 재정의 하는 것이다.
    # 핵심은 qs로 반환될 값을 조정하기 위해서 사용하는 것이다.
    def get_queryset(self):
        # self.request.user
        qs = super().get_queryset()
        # 만약 유저가 로그인하지 않은 상태라면
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)
        return qs


post_detail = PostDetailView.as_view()

# FBV 기반의 archive
# def archives_year(request, year):
#     return HttpResponse(f'{year}년 archives')

# CBV 기반의 archive
# 여기서 변수의 이름으로 지정해준 post_archive와 동일한 이름의 html 파일이 있어야 한다.
post_archive = ArchiveIndexView.as_view(
    model=Post,
    date_field='created_at',
    paginate_by=10
)

post_archive_year = YearArchiveView.as_view(
    model=Post, date_field='created_at', make_object_list=True)
