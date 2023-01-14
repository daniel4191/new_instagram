"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings


# CBV 사용 두번째 방법과 함께 사용하기 위해 생성한 클래스다.
class RootView(TemplateView):
    template_name = 'root.html'


urlpatterns = [
    # CBV 사용 첫번째 방법
    # templates를 루트에 등록해주고 그냥 root.html로 해보니깐 나오질 않더라.
    # path('', TemplateView.as_view(template_name='instagram/root.html'), name='root'),

    # CBV 사용 두번째 방법 - class 정의와 함께 사용한다.
    # path('', RootView.as_view(), name='root'),

    # URL Reverse방식 첫번째
    # path('', RedirectView.as_view(url='/instagram/'), name='root'),

    # URL Reverse방식 두번째 - Django 공식문서상에서는 이 방식이 선호된다.
    # <앱이름>:<앱단위의 urls.py에서 지정해준 name을 사용>
    path('', RedirectView.as_view(pattern_name='gram:post_list'), name='root'),
    path('admin/', admin.site.urls),
    path('blog1/', include('blog1.urls')),
    path('instagram/', include('gram.urls')),
    path('accounts/', include('accounts.urls')),
]

# 실질적으로는 DEBUG가 False, 즉 이미 서비스가 배포된 경우에는 static이 빈 리스트로 나온다고해서
# 명시적으로만 써주는거라고는 하는데
if settings.DEBUG:
    # 근본적으로 이것이 의미하는 바가 무엇인지는 어렴풋이 지레짐작으로만 알지, 디테일하게는 모르겠다.
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]

# settings.MEDIA_URL
# settings.MEDIA_ROOT
