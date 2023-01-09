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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog1/', include('blog1.urls')),
    path('instagram/', include('gram.urls'))
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
