from django.urls import path
from .views import (PostsList, PostDetail, Posts, PostCreateView, PostUpdateView, PostDeleteView, upgrade_me, CategoryListView, subscribe)

from .views import CategoryListView


app_name = 'news' #  запрос на сервере = NEWS: post_detail


urlpatterns = [
        path('', Posts.as_view()),
        path('<int:pk>', PostDetail.as_view(), name='post_detail'),
        path('search', PostsList.as_view()),
        path('add', PostCreateView.as_view(), name='post_create'),
        path('<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
        path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
        path('upgrade/', upgrade_me, name='upgrade'),
        path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
        path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
        path('posts/<int:pk>', PostsList.as_view(), name='post_list'),
]