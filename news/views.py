from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, User
from django.core.cache import cache
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category


class PostsList(ListView):
    model = Post
    template_name = 'posts_list.html'
    context_object_name = 'posts.html'
    ordering = [' -created_at']
    paginate_by = 2


class PostDetail(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        print(self.request.user.id)
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

# def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # subscribers = []
        # for category in kwargs['object'].category.all():
        #     subscribers += category.subscribers.all()
        # user = User.objects.filter(pk=self.request.user.pk).first() if self.request.user else None
        # context['need_subscribed'] = user not in subscribers
        # return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    template_name = 'news/post_create.html'
    form_class = PostForm


class Posts(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts.html.html'
    context_object_name = 'posts.html'
    ordering = [' -created_at']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exisits()
        return context


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    template_name = 'news/post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news')


class CategoryListView(Posts):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-crated_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})


## news : /post_detail.html/post_delete.html/post_create.html/category_list.html
## templates: /posts.html.html/post.html/posts_list.html/base.html
