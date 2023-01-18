from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView, CreateView
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm


from .forms import ProfileForm
from .models import Profile

User = get_user_model()
# Create your views here.

# FBV 방식
# @login_required
# def profile(request):
#     return render(request, 'accounts/profile.html')

# CBV 방식


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


profile = ProfileView.as_view()

# CBV
# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model = Profile
#     form_class = ProfileForm


# profile_edit = ProfileUpdateView.as_view()


# FBV
@login_required
def profile_edit(request):

    try:
        # 현재 이 코드는 Profile.objects.get(user=request.user)와 같은 의미다.
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_form.html', {
        'form': form
    })


class SignupView(CreateView):
    model = User,
    form_class = UserCreationForm,
    success_url = settings.LOGIN_REDIRECT_URL
    # 지금 사용하고 있는 signup이란것 자체가 사실 CBV이다.
    # 그렇다면 그 안에 model, template_name 등의 내부 함수가 있으니
    # 만약 TemplateDoesNotExist at /accounts/signup/auth/user_form.html
    # 라는 식으로 에러가 뜨고, 정확히 정해진 위치에 정해진 파일명을 지정할게 아니라면
    # template_name = 으로 커스텀 해주면 된다.
    template_name = 'accounts/signup_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        auth_login(self.request, user)
        return response


signup = SignupView.as_view()


def logout(request):
    pass
