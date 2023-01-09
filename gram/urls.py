from django.urls import path

from . import views

app_name = 'gram'

urlpatterns = [
    path('', views.post_list)
]
