from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.dates import ArchiveIndexView, YearArchiveView
from django.contrib import messages
from django.urls import reverse, reverse_lazy


from .models import Post
from .forms import PostForm

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
# class PostListView(LoginRequiredMixin, ListView):
#     model = Post
#     paginate_by = 10


# 이건 CBV 기반의 view를 만들때마다 urls를 만져줄 수 없으니, 그것을 대신하여 urls에 이미 post_list라고
# 등록이 되어있기 때문에 해주는 것이다.
# post_list = PostListView.as_view()


# FBV 기반
@login_required
def post_list(request):
    qs = Post.objects.all()
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(message__icontains=q)

    messages.info(request, 'messages test')
    # gram/templates/gram/post_list.html
    return render(request, 'gram/post_list.html', {
        'post_list': qs,
        'q': q
    })


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


# FBV
# @login_required
# def post_new(request):
#     # 만약 html의 input등을 통해서 데이터를 전달받기를 원한다면 정의해주어야 함.
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # commit이 True여야 "model instance"가 호출이 된다고 한다.
#             # 구체적으로는 잘 모르겠다.
#             # 하지만 만약에 commit 값이 False면 실제 데이터베이스에 save가 안된다고 한다.
#             # 또 하지만 commit을 False로 하더라도 post = form.save(commit=False)
#             # 바로 다음 인자가 post.save()면 저장된다고 한다.
#             # post = form.save(commit=True)

#             post = form.save()
#             # ***매우중요****
#             # 여기서 redirect로 post를 받았다.
#             # post는 위에서 여러가지 과정을 거쳐서 "유효하고" "저장된" form을 post = form.save()로 처리해주었다.
#             # form은 위에서 PostForm으로 진행을 했으며
#             # PostForm은 forms.py에서 Post model을 상속받았다.
#             # Post model을 models.py에서 보게 되면
#             # get_absolute_url이 설정되어있고
#             # 그 get_absolute_url은 post_detail페이지로 이동되게끔 (여기서는) 설정되었으니
#             # 그렇게 이동이 된다.
#             return redirect(post)
#     else:
#         form = PostForm()

#     return render(request, 'gram/post_form.html', {
#         'form': form,
#         'post': None
#     })

# CBV
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        messages.success(self.request, '포스팅을 저장했습니다.')
        return super().form_valid(form)


post_new = PostCreateView.as_view()

# 이 데코레이터 하나만으로 로그인되어있다는 전제가 분명해진다.
# 로그인을 안하면 접근이 안된다.


# FBV
# @login_required
# def post_edit(request, pk):
#     # pk 인자에 해당하는 인스턴스 (인스턴스는 쉽게 객체의 실체화 라고 생각하면 된다.)
#     post = get_object_or_404(Post, pk=pk)

#     # 작성자 check Tip
#     if post.author != request.user:
#         messages.error(request, '작성자만 수정할 수 있습니다.')
#         return redirect(post)

#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         # forms.py설명의 연장선상이다 (Integrity Error관련)
#         # 유효한 정보들이 들어가야하고
#         if form.is_valid():
#             # 여기서 바로 세이브 해주게 되면 노출되어야하는 필드와 일치하지 않으니 에러가 날것이다.
#             # post = form.save()
#             # 그걸 위해서 commit = False를 우선해주고
#             post = form.save(commit=False)
#             # 필수 필드를 여기서 처리해준다.(이 경우에는 author)
#             # 현재 로그인된 User 인스턴스 즉, 반드시 로그인이 되어있다는 전제가 되어야한다.
#             post.author = request.user
#             post.save()
#             return redirect(post)

#     else:
#         form = PostForm(instance=post)

#     return render(request, 'gram/post_form.html', {
#         'form': form,
#         'post': post
#     })


# CBV

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        messages.success(self.request, '포스팅을 수정했습니다.')
        return super().form_valid(form)


post_edit = PostUpdateView.as_view()


# FBV
# @login_required
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     if request.method == 'POST':
#         post.delete()
#         messages.success(request, '포스팅을 삭제했습니다.')
#         return redirect('gram:post_list')
#     return render(request, 'gram/post_confirm_delete.html', {
#         'post': post
#     })


# CBV
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # 삭제 성공시 이동 경로 방법 1
    # success_url = '/instagram/'

    # 삭제 성공시 이동 경로 방법 2
    # def get_success_url(self):
    #     return reverse('gram:post_list')

    # 삭제 성공시 이동 경로 방법 3
    success_url = reverse_lazy('gram:post_list')


post_delete = PostDeleteView.as_view()
