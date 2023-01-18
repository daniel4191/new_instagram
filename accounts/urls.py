from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .forms import LoginForm

app_name = 'accounts'

urlpatterns = [
    # 기본 셋팅에 대해 templates_name은 'registration/login.html'이 되기때문에 (장고 공식 깃허브 코드에서 확인 가능)
    # 내가 혹시라도 다른 경로로 쓸거라면 이렇게 as_view()안의 인자를 커스터마이징 해주어야 한다.
    path('login/', LoginView.as_view(
        form_class=LoginForm,
        template_name='accounts/login_form.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('signup/', views.signup, name='signup'),
]
