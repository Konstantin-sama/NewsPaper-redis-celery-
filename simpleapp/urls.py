from django.urls import path
# Импортируем созданное нами представление
from django.urls import path
from .views import (PostList, PostDetail, PostSearch, PostAdd, PostUpdateView, PostDeleteView, add_subscribe, del_subscribe)


urlpatterns = [
        path('', PostList.as_view()),
        path('<int:pk>', PostDetail.as_view(), name='post_detail'),
        path('search', PostSearch.as_view()),
        path('add', PostAdd.as_view(), name='post_create'),
        path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
        path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
        path('<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
        path('<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
]